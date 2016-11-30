import os
basedir = os.path.abspath(os.path.dirname(__file__))

# database location
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db/app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
