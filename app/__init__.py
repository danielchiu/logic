from flask import * # TODO actually look at imports 

from flask_sqlalchemy import SQLAlchemy

from views import *

app = Flask(__name__)
app.register_blueprint(views) # TODO forgot what this does

#app.config.from_object('config') # TODO wat
#db = SQLAlchemy(app) # TODO wat

app.secret_key = "JILFEfjwioje234fe#$DE("

#db.create_all()
