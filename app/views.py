from flask import * # TODO actually look at imports
from models import User, Game
from app import db
import logging

views = Blueprint("views",__name__)
try:
    logging.basicConfig(filename = "/home/chiud/logic/debug/error.log")
except IOError:
    pass

@views.route("/")
def homepage():
    # logging.error("this is an error")
    user = None
    if "user" in session:
        user = session["user"]
    return render_template("homepage.html", user = user)

@views.route("/login", methods = ["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user is None:
            error = "No such user \"%s\" exists" % request.form["username"]
        else:
            # TODO check username for length
            session["user"] = user.username # TODO is there a way to make it whole User class
            return redirect(url_for("views.homepage"))
    return render_template("login.html", error = error)

@views.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("views.homepage"))

@views.route("/register", methods = ["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user is not None:
            error = "The user \"%s\" already exists" % user.username
        else:
            user = User(request.form["username"])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("views.homepage"))
    return render_template("register.html", error = error)

def refresh(game):
    db.session.delete(game)
    db.session.commit()
    return Game(game.name, game.players, game.hands, game.log, game.current, game.state) # TODO really hacky way to get around the pickletype issue
def insert(game):
    db.session.add(game)
    for player in game.players:
        user = User.query.filter_by(username=player).first()
        if user is None:
            pass # TODO this shouldn't happen once users must exist
        else:
            game.users.append(user)
    db.session.commit()

@views.route("/newgame", methods = ["GET", "POST"])
def newgame():
    error = None
    if request.method == "POST":
        game = Game.query.filter_by(name=request.form["name"]).first()
        if game is not None:
            error = "The game \"%s\" already exists" % game.name
        else:
            game = Game(request.form["name"],[request.form["p1"],request.form["p2"],request.form["p3"],request.form["p4"]])
            # TODO make sure all the above are valid
            insert(game)
            return redirect(url_for("views.game", name = request.form["name"]))
    return render_template("newgame.html", error = error)

@views.route("/games")
def games():
    user = session["user"]
    games = User.query.filter_by(username=user).first().games
    completed = [x for x in games if x.state==4]
    games = [x for x in games if not x.state==4]
    myturn = [x for x in games if (x.index(user)==x.current and x.state>=0) or ((-x.state)&(1<<x.index(user)))>0]
    games = [x for x in games if not ((x.index(user)==x.current and x.state>=0) or ((-x.state)&(1<<x.index(user)))>0)]
    return render_template("games.html", user = user, myturn = myturn, games = games, completed = completed)

@views.route("/game/<name>", methods = ["GET", "POST"])
def game(name):
    game = Game.query.filter_by(name=name).first()
    if game is None:
        return redirect(url_for("views.homepage")) # TODO give some error message
    user = None
    if "user" in session:
        user = session["user"]
    ind = game.index(user)

    if request.method == "POST":
        if int(request.form["loglen"]) != len(game.log):
            return redirect(url_for("views.game", name = name))

    if game.state==4:
        return render_template("game-over.html", name = name, user = user, game = game)
    if game.state<0:
        if request.method == "POST":
            swapped = request.form["swapped"]
            game = refresh(game)
            for val in swapped:
                for i in range(6):
                    if game.hands[ind].cards[i].val == val:
                        game.hands[ind].cards[i], game.hands[ind].cards[i+1] = game.hands[ind].cards[i+1], game.hands[ind].cards[i]
                        break
            game.state+=(1<<ind)
            game.log.append(user+" has finished ordering cards")
            insert(game)
            return redirect(url_for("views.game", name = name))
        done = (ind==-1 or ((-game.state)&(1<<ind))==0)
        return render_template("game-order.html", name = name, user = user, game = game, done = done)

    if request.method == "POST" and request.form["card"]=="declare":
        game = refresh(game)
        game.state = 3
        game.current = ind
        for i in range(6):
            game.hands[ind].cards[i].flipped = True
        game.log.append(user+" declared!")
        insert(game)
        return redirect(url_for("views.game",name = name))
    if ind == game.current:
        if game.state==0:
            if request.method == "POST":
                which = int(request.form["card"])
                game = refresh(game)
                game.state = 1
                game.current = (game.current+2)%4
                game.hands[ind].cards[which-1].secret = True
                game.log.append(user+" passed card "+str(which))
                insert(game)
                return redirect(url_for("views.game", name = name))
            return render_template("game-pass.html", name = name, user = user, game = game)
        if game.state == 1:
            if request.method == "POST":
                player = int(request.form["card"][0])
                which = int(request.form["card"][1])
                value = request.form["card"][2]
                game = refresh(game)
                success = False
                if game.hands[(ind+player)%4].cards[which-1].val == value:
                    success = True
                if success:
                    game.state = 0
                    game.current = (game.current+3)%4
                    game.hands[(ind+player)%4].cards[which-1].flipped = True
                    game.log.append(user+" correctly guessed "+game.players[(ind+player)%4]+"'s card "+str(which))
                else:
                    game.state = 2
                    game.log.append(user+" incorrectly guessed "+game.players[(ind+player)%4]+"'s card "+str(which)+" as "+value)
                insert(game)
                return redirect(url_for("views.game", name = name))
            return render_template("game-guess.html", name = name, user = user, game = game)
        if game.state == 2:
            if request.method == "POST":
                which = int(request.form["card"])
                game = refresh(game)
                game.state = 0
                game.current = (game.current+3)%4
                game.hands[ind].cards[which-1].flipped = True
                game.log.append(user+" revealed card "+str(which))
                insert(game)
                return redirect(url_for("views.game", name = name))
            return render_template("game-reveal.html", name = name, user = user, game = game)
        if game.state == 3:
            if request.method == "POST":
                player = int(request.form["card"][0])
                which = int(request.form["card"][1])
                value = request.form["card"][2]
                game = refresh(game)
                success = False
                if game.hands[(ind+player)%4].cards[which-1].val == value:
                    success = True
                if success:
                    game.hands[(ind+player)%4].cards[which-1].flipped = True
                    game.log.append(user+" correctly guessed "+game.players[(ind+player)%4]+"'s card "+str(which))
                else:
                    game.state = 4
                    game.players+=[game.players[(ind+1)%4],game.players[(ind+3)%4]]
                    game.log.append(user+" incorrectly guessed "+game.players[(ind+player)%4]+"'s card "+str(which)+" as "+value)
                    game.log.append(user+" made a mistake while declaring!")
                    game.log.append(game.players[(ind+1)%4]+" and "+game.players[(ind+3)%4]+" win!")
                insert(game)
                return redirect(url_for("views.game", name = name))
            done = True
            for i in range(4):
                for j in range(6):
                    if not game.hands[i].cards[j].flipped:
                        done = False
            if done:
                game = refresh(game)
                game.state = 4
                game.players+=[game.players[ind],game.players[(ind+2)%4]]
                game.log.append(user+" has successfully named every card!")
                game.log.append(user+" and "+game.players[(ind+2)%4]+" win!")
                insert(game)
                return redirect(url_for("views.game", name = name))
            return render_template("game-call.html", name = name, user = user, game = game)
    if request.method == "POST":
        return redirect(url_for("views.homepage")) # TODO give some error message
    return render_template("game-base.html", name = name, user = user, game = game)
