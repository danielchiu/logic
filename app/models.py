from app import db

games = db.Table('games',
    db.Column('user_id', db.Integer, db.ForeignKey('game.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True) # TODO index=?

    playing = db.relationship('Game', secondary=games, backref='players')
    
    def __init__(self, username):
        self.username = username

    def __str___(self):
        return '<User %s>' % self.username

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # using id as game_id
    
    def __str__(self):
        return '<Game %d>' % self.id


