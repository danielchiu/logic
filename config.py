import os
basedir = os.path.abspath(os.path.dirname(__file__))

# database location — override with DATABASE_URL env var for production
# Render uses postgres:// but SQLAlchemy 2.0 requires postgresql://
database_url = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(basedir, 'db/app.db')
)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_TRACK_MODIFICATIONS = False
