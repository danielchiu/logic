"""One-shot migration: fix swapped user_id/game_id values in the `status` table.

Historically the `status` association table was declared with the FK targets
swapped:

    Column('user_id', ForeignKey('game.id'))   # actually stored game IDs
    Column('game_id', ForeignKey('user.id'))   # actually stored user IDs

The schema has been corrected so that `user_id` references `user.id` and
`game_id` references `game.id`. Existing rows therefore have their values in
the wrong columns and need to be swapped.

Run once against any database created before the fix:

    python -m scripts.migrate_status_columns
"""
from sqlalchemy import text

from app import app, db


def migrate():
    with app.app_context():
        with db.engine.begin() as conn:
            # Swap the two columns in-place. SQLite supports this via a temp
            # column; for portability we use a generic three-step swap.
            conn.execute(text("ALTER TABLE status ADD COLUMN _tmp_id INTEGER"))
            conn.execute(text("UPDATE status SET _tmp_id = user_id"))
            conn.execute(text("UPDATE status SET user_id = game_id"))
            conn.execute(text("UPDATE status SET game_id = _tmp_id"))
            # SQLite < 3.35 cannot DROP COLUMN; leave the temp column in place
            # there. On databases that support it, drop it.
            try:
                conn.execute(text("ALTER TABLE status DROP COLUMN _tmp_id"))
            except Exception:
                pass
        print("status table migrated: user_id/game_id values swapped.")


if __name__ == "__main__":
    migrate()
