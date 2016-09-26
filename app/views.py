from flask import * # TODO actually look at imports
from game import Master
from models import User, Game
from app import db

views = Blueprint("views",__name__)

@views.route("/")
def homepage():
    user = None
    if "user" in session:
        user = session["user"]
    return render_template("homepage.html",user=user)

@views.route("/login", methods = ["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user is None:
            error = "No such user exists"
        else:
            # TODO check username for length
            session["user"] = user.username # TODO is there a way to make it whole User class
            return redirect("/")
    return render_template("login.html",error = error)

@views.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

@views.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(request.form["username"])
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")

@views.route("/newgame", methods = ["GET", "POST"])
def newgame():
    if request.method == "POST":
        game = Game(request.form["name"],Master().hands, \
                    [request.form["p1"],request.form["p2"],request.form["p3"],request.form["p4"]])
        # TODO make sure all the above are valid
        db.session.add(game)
        db.session.commit()
        return redirect("/") # TODO route to game instead
    return render_template("newgame.html")

@views.route("/game/<name>")
def game(name):
    game = Game.query.filter_by(name=name).first()
    if game is None:
        return render_template("game.html", name = name, grid = Master().grid()) # TODO give some error message
    user = None
    if "user" in session:
        user = session["user"]
    ind = game.index(user)
    print "accessing player %d" % ind
    return render_template("game.html", name = name, grid = Master(game.hands).grid())
