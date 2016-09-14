from flask import * # TODO actually look at imports 

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config') # TODO wat

db = SQLAlchemy(app) # TODO wat

app.secret_key = "JILFEfjwioje234fe#$DE("
