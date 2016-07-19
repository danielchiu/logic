from flask import * # TODO actually look at imports 

from views import *

app = Flask(__name__)
app.register_blueprint(views)

app.secret_key = "JILFEfjwioje234fe#$DE("

app.run()
