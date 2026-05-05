# Compatibility shim for old pickle data.
#
# Before the Python 3 migration (PR #1), Card and Hand lived at the
# top-level 'game' module.  Existing PickleType columns in the database
# store references to 'game.Card' and 'game.Hand'.  When unpickling,
# Python needs to find those classes at the original module path.
#
# This shim is used by the migration scripts (migrate_sqlite_to_postgres,
# migrate_pickle_to_json) to deserialize old pickle data. It can be
# removed once all pickle data has been converted to JSON.

from app.game import Card, Hand, values, suits  # noqa: F401
