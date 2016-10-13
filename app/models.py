from app import db
from game import Card, Hand, values, suits
import random

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
    name = db.Column(db.String, index=True, unique=True)
    hands = db.Column(db.PickleType)
    players = db.Column(db.PickleType)
    current = db.Column(db.Integer)
    state = db.Column(db.Integer) # 0 means passing, 1 means guessing

    def __init__(self, name, players, hands = None, current = None, state = None):
        self.name = name

        self.players = players

        self.hands = hands
        if hands == None:
            deck = []
            for val in values:
                for suit in suits:
                    deck.append(Card(val,suit))
            random.shuffle(deck)

            self.hands = []
            for i in range(4):
                self.hands.append(Hand(deck[i*6:i*6+6]))

        self.current = current
        if self.current == None:
            self.current = random.randint(0,3)
        self.state = state
        if self.state == None:
            self.state = 0

    def __str__(self):
        return '<Game %s: %s %s %s %s>' % (self.name, str(self.players))

    def index(self, player):
        try:
            return self.players.index(player)
        except ValueError:
            return -1

    def grid(self, player):
        number = self.index(player)
        hands = self.hands
        players = self.players
        if number >= 0:
            hands = hands[number:]+hands[:number]
            players = players[number:]+players[:number]

        res = [None]*64
        for i in range(6):
            res[57+i] = hands[0].cards[i]
            if number >= 0:
                res[57+i].flipped = True
        res[50] = 'R'+players[0]
        for i in range(6):
            res[55-8*i] = hands[1].cards[i]
        res[46] = 'U'+players[1]
        for i in range(6):
            res[6-i] = hands[2].cards[i]
            if number >= 0 and res[6-i].secret:
                res[6-i].flipped = True
        res[13] = 'L'+players[2]
        for i in range(6):
            res[8+8*i] = hands[3].cards[i]
        res[17] = 'D'+players[3]
        return res
