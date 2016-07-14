from flask import * # TODO actually look at imports 

from views import *

app = Flask(__name__)
app.register_blueprint(views)

@app.route("/game/<int:id>") # just here for memory of the <int:id> thing
def getGame(id):
    return render_template('game.html', id=id)

app.secret_key = "JILFEfjwioje234fe#$DE("

app.run()
