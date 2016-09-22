from app import db

games = db.Table('games',
    db.Column('user_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True) # TODO what is index

    playing = db.relationship('Game', secondary=games, backref='players')
    
    def __init__(self, username):
        self.username = username

    def __str___(self):
        return '<User %s>' % self.username

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    p1 = db.Column(db.String, index=True)
    p2 = db.Column(db.String, index=True)
    p3 = db.Column(db.String, index=True)
    p4 = db.Column(db.String, index=True)
    hands = db.Column(db.PickleType)
    
    def __init__(self, name, hands, p1, p2, p3, p4):
        self.name = name
        self.p1, self.p2, self.p3, self.p4 = p1, p2, p3, p4 
        self.hands = hands 

    def __str__(self):
        return '<Game %s: %s %s %s %s>' % (self.name, self.p1, self.p2, self.p3, self.p4)
