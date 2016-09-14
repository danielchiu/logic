from flask import * # TODO actually look at imports 

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#from views import views 
#app.register_blueprint(views) # TODO wrong place

app.config.from_object('config') # TODO wat

db = SQLAlchemy(app) # TODO wat

app.secret_key = "JILFEfjwioje234fe#$DE("

#db.create_all()
