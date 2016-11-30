from flask import * # TODO actually look at imports 

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

app.secret_key = "JILFEfjwioje234fe#$DE(" # TODO add an actually random string
