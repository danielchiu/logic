from app import db

status = db.Table('status',
    db.Column('user_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True) # TODO what is index

    games = db.relationship('Game', secondary=status, backref='users')
    
    def __init__(self, username):
        self.username = username

    def __str___(self):
        return '<User %s>' % self.username

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    hands = db.Column(db.PickleType)
    players = db.Column(db.PickleType)
    
    def __init__(self, name, hands, players):
        self.name = name
        self.hands = hands 
        self.players = players

    def __str__(self):
        return '<Game %s: %s %s %s %s>' % (self.name, str(self.players))

    def index(self, player):
        try:
            return self.players.index(player)
        except ValueError:
            return -1

    def rotate(self, number):
        self.hands = self.hands[number:]+self.hands[:number]
        self.players = self.players[number:]+self.players[:number]
