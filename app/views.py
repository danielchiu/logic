from flask import * # TODO actually look at imports
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
        game = Game(request.form["name"],[request.form["p1"],request.form["p2"],request.form["p3"],request.form["p4"]])
        # TODO make sure all the above are valid
        db.session.add(game)
        db.session.commit()
        return redirect("/game/"+request.form["name"])
    return render_template("newgame.html")

def refresh(game):
    db.session.delete(game)
    db.session.commit()
    return Game(game.name, game.players, game.hands, game.current, game.state) # TODO really hacky way to get around the pickletype issue


@views.route("/game/<name>", methods = ["GET", "POST"])
def game(name):
    game = Game.query.filter_by(name=name).first()
    if game is None:
        return redirect("/") # TODO give some error message
    user = None
    if "user" in session:
        user = session["user"]
    if game.state==5:
        return render_template("game-over.html", name = name, user = user, game = game)
    ind = game.index(user)
    if ind == game.current:
        if game.state==0:
            if request.method == "POST":
                which = int(request.form["card"])
                game = refresh(game)
                game.state = 1
                game.current = (game.current+2)%4
                game.hands[ind].cards[which].secret = True
                db.session.add(game)
                db.session.commit()
                return redirect("/game/"+name)
            return render_template("game-pass.html", name = name, user = user, game = game)
        if game.state == 1:
            if request.method == "POST":
                player = int(request.form["card"][0])
                which = int(request.form["card"][1])
                value = request.form["card"][2]
                game = refresh(game)
                success = False
                if game.hands[(ind+player)%4].cards[which].val == value:
                    success = True
                if success:
                    game.state = 0
                    game.current = (game.current+3)%4
                    game.hands[(ind+player)%4].cards[which].flipped = True
                else:
                    game.state = 2
                db.session.add(game)
                db.session.commit()
                return redirect("/game/"+name)
            return render_template("game-guess.html", name = name, user = user, game = game)
        if game.state == 2:
            if request.method == "POST":
                which = int(request.form["card"])
                game = refresh(game)
                game.state = 0
                game.current = (game.current+3)%4
                game.hands[ind].cards[which].flipped = True
                db.session.add(game)
                db.session.commit()
                return redirect("/game/"+name)
            return render_template("game-reveal.html", name = name, user = user, game = game)
        if game.state == 3:
            if request.method == "POST":
                player = int(request.form["card"][0])
                which = int(request.form["card"][1])
                value = request.form["card"][2]
                game = refresh(game)
                success = False
                if game.hands[(ind+player)%4].cards[which].val == value:
                    success = True
                if success:
                    game.hands[(ind+player)%4].cards[which].flipped = True
                else:
                    game.state = 5
                    game.players = [game.players[(ind+1)%4],game.players[(ind+3)%4]]
                db.session.add(game)
                db.session.commit()
                return redirect("/game/"+name)
            done = True
            for i in range(4):
                for j in range(6):
                    if not game.hands[i].cards[j].flipped:
                        done = False
            if done:
                game = refresh(game)
                game.state = 5
                game.players = [game.players[ind],game.players[(ind+2)%4]]
                db.session.add(game)
                db.session.commit()
                return redirect("/game/"+name)
            return render_template("game-declare.html", name = name, user = user, game = game)
    if request.method == "POST":
        return redirect("/") # TODO give some error message
    return render_template("game-base.html", name = name, user = user, game = game)
