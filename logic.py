# WSGI entrypoint — used by Gunicorn / production servers
from app import app as application
from app import db
from app.views import views

application.register_blueprint(views)

with application.app_context():
    db.create_all()
