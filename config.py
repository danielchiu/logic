import os
basedir = os.path.abspath(os.path.dirname(__file__))

# database location — override with DATABASE_URL env var for production
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(basedir, 'db/app.db')
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
