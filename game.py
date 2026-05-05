# Compatibility shim for old pickle data.
#
# Before the Python 3 migration (PR #1), Card and Hand lived at the
# top-level 'game' module.  Existing PickleType columns in the database
# store references to 'game.Card' and 'game.Hand'.  When SQLAlchemy
# deserializes them, Python needs to find those classes at the original
# module path.  Re-exporting them here satisfies that requirement.

from app.game import Card, Hand, values, suits  # noqa: F401
