"""Migrate data from a SQLite database to PostgreSQL.

Usage:
    DATABASE_URL=postgresql://user:pass@host/db python -m scripts.migrate_sqlite_to_postgres [sqlite_path]

Arguments:
    sqlite_path  Path to the SQLite database file (default: db/app.db)

The target PostgreSQL database is read from the DATABASE_URL environment
variable (which the app already uses in production). Tables are created
automatically if they don't exist.

This script is idempotent for users (skips duplicates by username) and
games (skips duplicates by name). Run it once after deploying to Render
to backfill your existing game data.
"""
import json
import os
import pickle
import sys

from sqlalchemy import create_engine, text

# The old SQLite data was pickled when Card/Hand lived at the top-level
# 'game' module. Ensure that module path is importable for unpickling.
import game  # noqa: F401


def pickle_to_json(raw, col_name):
    """Deserialize pickle bytes from SQLite and return a JSON string."""
    if raw is None:
        return None
    obj = pickle.loads(raw)
    if col_name == 'hands':
        # List of Hand objects → list of lists of card dicts
        result = []
        for hand in obj:
            cards = []
            for card in hand.cards:
                cards.append({
                    'val': card.val,
                    'suit': card.suit,
                    'flipped': card.flipped,
                    'secret': card.secret,
                    'private': card.private,
                })
            result.append(cards)
        return json.dumps(result)
    # players, log, chat, notes are plain Python lists/dicts
    return json.dumps(obj)


def migrate(sqlite_path="db/app.db"):
    pg_url = os.environ.get("DATABASE_URL", "")
    if pg_url.startswith("postgres://"):
        pg_url = pg_url.replace("postgres://", "postgresql://", 1)
    if not pg_url.startswith("postgresql://"):
        print("ERROR: DATABASE_URL must be a postgresql:// connection string.")
        print("  Example: DATABASE_URL=postgresql://user:pass@host:5432/dbname")
        sys.exit(1)

    if not os.path.exists(sqlite_path):
        print(f"ERROR: SQLite file not found: {sqlite_path}")
        sys.exit(1)

    sqlite_url = f"sqlite:///{os.path.abspath(sqlite_path)}"
    sqlite_engine = create_engine(sqlite_url)

    # Read all data from SQLite
    with sqlite_engine.connect() as src:
        users = src.execute(text("SELECT id, username FROM user")).fetchall()
        games = src.execute(text(
            "SELECT id, name, hands, players, log, current, state, chat, notes "
            "FROM game"
        )).fetchall()
        # The original schema had the FK references swapped:
        #   Column 'user_id' -> ForeignKey('game.id')
        #   Column 'game_id' -> ForeignKey('user.id')
        # So in the SQLite file, 'user_id' actually stores game IDs and
        # vice versa. Read them swapped so they map correctly to the
        # fixed schema.
        statuses = src.execute(text(
            "SELECT game_id AS user_id, user_id AS game_id FROM status"
        )).fetchall()

    print(f"Read from SQLite: {len(users)} users, {len(games)} games, "
          f"{len(statuses)} status links")

    # Use the app's engine (pointed at PostgreSQL via DATABASE_URL) to create
    # tables and insert data, so the schema matches the ORM models exactly.
    from app import app, db
    from app.views import views
    app.register_blueprint(views)

    with app.app_context():
        db.create_all()
        print("PostgreSQL tables created/verified")

        with db.engine.begin() as dst:
            # Insert users (skip duplicates)
            for user in users:
                existing = dst.execute(
                    text('SELECT id FROM "user" WHERE username = :u'),
                    {"u": user[1]}
                ).fetchone()
                if existing:
                    print(f"  Skipping existing user: {user[1]}")
                    continue
                dst.execute(
                    text('INSERT INTO "user" (id, username) VALUES (:id, :username)'),
                    {"id": user[0], "username": user[1]}
                )
                print(f"  Migrated user: {user[1]}")

            # Insert games (skip duplicates).
            # Use 'game_row' to avoid shadowing the 'game' compatibility-shim
            # module imported above for pickle class resolution.
            for game_row in games:
                existing = dst.execute(
                    text("SELECT id FROM game WHERE name = :n"),
                    {"n": game_row[1]}
                ).fetchone()
                if existing:
                    print(f"  Skipping existing game: {game_row[1]}")
                    continue
                # SQLite stores pickle bytes; PostgreSQL now uses JSON.
                # Deserialize pickle and convert to JSON (see pickle_to_json).
                dst.execute(
                    text(
                        'INSERT INTO game (id, name, hands, players, log, '
                        '"current", state, chat, notes) '
                        'VALUES (:id, :name, CAST(:hands AS json), CAST(:players AS json), CAST(:log AS json), '
                        ':current, :state, CAST(:chat AS json), CAST(:notes AS json))'
                    ),
                    {
                        "id": game_row[0],
                        "name": game_row[1],
                        "hands": pickle_to_json(game_row[2], 'hands'),
                        "players": pickle_to_json(game_row[3], 'players'),
                        "log": pickle_to_json(game_row[4], 'log'),
                        "current": game_row[5],
                        "state": game_row[6],
                        "chat": pickle_to_json(game_row[7], 'chat'),
                        "notes": pickle_to_json(game_row[8], 'notes'),
                    }
                )
                print(f"  Migrated game: {game_row[1]}")

            # Insert status links (skip duplicates and orphaned references)
            migrated_links = 0
            skipped_orphans = 0
            for status in statuses:
                uid, gid = status[0], status[1]
                # Skip orphaned references — SQLite doesn't enforce FKs, so
                # deleted users/games may still have dangling status rows.
                user_exists = dst.execute(
                    text('SELECT 1 FROM "user" WHERE id = :id'),
                    {"id": uid}
                ).fetchone()
                game_exists = dst.execute(
                    text("SELECT 1 FROM game WHERE id = :id"),
                    {"id": gid}
                ).fetchone()
                if not user_exists or not game_exists:
                    skipped_orphans += 1
                    continue
                existing = dst.execute(
                    text(
                        "SELECT 1 FROM status "
                        "WHERE user_id = :uid AND game_id = :gid"
                    ),
                    {"uid": uid, "gid": gid}
                ).fetchone()
                if existing:
                    continue
                dst.execute(
                    text("INSERT INTO status (user_id, game_id) VALUES (:uid, :gid)"),
                    {"uid": uid, "gid": gid}
                )
                migrated_links += 1
            print(f"  Migrated {migrated_links} status links")
            if skipped_orphans:
                print(f"  Skipped {skipped_orphans} orphaned status links "
                      f"(referenced non-existent users or games)")

            # Reset PostgreSQL sequences so new inserts get correct IDs
            max_user = dst.execute(
                text('SELECT COALESCE(MAX(id), 0) FROM "user"')
            ).scalar()
            max_game = dst.execute(
                text("SELECT COALESCE(MAX(id), 0) FROM game")
            ).scalar()
            if max_user > 0:
                dst.execute(text(f"SELECT setval('user_id_seq', {max_user}, true)"))
            if max_game > 0:
                dst.execute(text(f"SELECT setval('game_id_seq', {max_game}, true)"))

    print(f"\nMigration complete: {len(users)} users, {len(games)} games, "
          f"{len(statuses)} status links")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "db/app.db"
    migrate(path)
