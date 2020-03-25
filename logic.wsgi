# setup for web server
import sys

# directory path
project_home = '/home/tuxianeer/logic'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
app_home = '/home/tuxianeer/logic/app'
if app_home not in sys.path:
    sys.path = [app_home] + sys.path

from app import app as application
from app import db
from app.views import views

db.create_all()

application.register_blueprint(views)
