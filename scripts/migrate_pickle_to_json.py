"""Convert PickleType columns in the game table to JSON.

Usage:
    DATABASE_URL=postgresql://user:pass@host/db python -m scripts.migrate_pickle_to_json

This script reads existing pickle-serialized data from the hands, players,
log, chat, and notes columns, deserializes them, and writes back JSON.

It also ALTERs the column types from BYTEA (pickle) to JSONB.

Run this ONCE after deploying the code that switches from PickleType to JSON.
The script is idempotent — it detects whether columns are already JSONB and
skips the ALTER if so.
"""
import json
import os
import pickle
import sys

from sqlalchemy import create_engine, text

# The pickle data references Card/Hand from the top-level 'game' module.
# Ensure that module path is importable for unpickling.
import game  # noqa: F401


def migrate():
    pg_url = os.environ.get("DATABASE_URL", "")
    if pg_url.startswith("postgres://"):
        pg_url = pg_url.replace("postgres://", "postgresql://", 1)
    if not pg_url.startswith("postgresql://"):
        print("ERROR: DATABASE_URL must be a postgresql:// connection string.")
        sys.exit(1)

    engine = create_engine(pg_url)

    with engine.begin() as conn:
        # Check current column types
        col_types = {}
        rows = conn.execute(text(
            "SELECT column_name, data_type FROM information_schema.columns "
            "WHERE table_name = 'game' AND column_name IN "
            "('hands', 'players', 'log', 'chat', 'notes')"
        )).fetchall()
        for row in rows:
            col_types[row[0]] = row[1]

        if not col_types:
            print("ERROR: No game table found or no pickle columns found.")
            sys.exit(1)

        print(f"Current column types: {col_types}")

        # If all columns are already jsonb, nothing to do
        if all(t == 'jsonb' for t in col_types.values()):
            print("All columns are already JSONB. Nothing to do.")
            return

        # Read all games
        games = conn.execute(text("SELECT id, hands, players, log, chat, notes FROM game")).fetchall()
        print(f"Found {len(games)} games to migrate")

        if len(games) == 0:
            # No data — just ALTER the columns
            for col in ['hands', 'players', 'log', 'chat', 'notes']:
                if col_types.get(col) != 'jsonb':
                    conn.execute(text(
                        f'ALTER TABLE game ALTER COLUMN "{col}" TYPE JSONB '
                        f'USING "{col}"::text::jsonb'
                    ))
                    print(f"  ALTERed {col} to JSONB (no data)")
            print("Migration complete (no data to convert).")
            return

        # For each game, deserialize pickle data and prepare JSON
        for game in games:
            game_id = game[0]
            updates = {}

            for i, col in enumerate(['hands', 'players', 'log', 'chat', 'notes'], start=1):
                raw = game[i]
                if raw is None:
                    updates[col] = None
                    continue

                if col_types.get(col) == 'jsonb':
                    # Already JSON, skip
                    continue

                # Deserialize pickle bytes
                try:
                    obj = pickle.loads(raw)
                except Exception as e:
                    print(f"  WARNING: Could not unpickle {col} for game {game_id}: {e}")
                    updates[col] = None
                    continue

                # Convert to JSON-serializable format
                if col == 'hands':
                    # List of Hand objects → list of lists of card dicts
                    json_val = []
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
                        json_val.append(cards)
                else:
                    # players, log, chat, notes are already plain Python
                    json_val = obj

                updates[col] = json.dumps(json_val)

            # Write JSON strings back to the row (still BYTEA columns at this point)
            if updates:
                set_clauses = []
                params = {"gid": game_id}
                for col, val in updates.items():
                    if col_types.get(col) == 'jsonb':
                        continue
                    set_clauses.append(f'"{col}" = :{col}')
                    params[col] = val.encode('utf-8') if val is not None else None
                if set_clauses:
                    conn.execute(
                        text(f"UPDATE game SET {', '.join(set_clauses)} WHERE id = :gid"),
                        params
                    )
                    print(f"  Converted game {game_id} pickle → JSON bytes")

        # Now ALTER columns from BYTEA to JSONB
        for col in ['hands', 'players', 'log', 'chat', 'notes']:
            if col_types.get(col) != 'jsonb':
                conn.execute(text(
                    f'ALTER TABLE game ALTER COLUMN "{col}" TYPE JSONB '
                    f'USING convert_from("{col}", \'UTF8\')::jsonb'
                ))
                print(f"  ALTERed {col} from {col_types.get(col, 'unknown')} to JSONB")

    print("\nMigration complete! All pickle columns are now JSONB.")


if __name__ == "__main__":
    migrate()
