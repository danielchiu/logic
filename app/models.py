import random

from sqlalchemy import types

from app import db
from .game import Card, Hand, values, suits


class HandsJSON(types.TypeDecorator):
    """Store a list of Hand objects as JSON.

    DB representation: [[{val, suit, flipped, secret, private}, ...], ...]
    Python representation: [Hand, Hand, Hand, Hand]
    """
    impl = types.JSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return [hand.to_dict() for hand in value]

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return [Hand.from_dict(card_list) for card_list in value]

# keeps track of which games a user is playing (and which users are playing a game)
status = db.Table('status',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
)

'''
class for a user
    games = list of games currently playing
'''
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)

    games = db.relationship('Game', secondary=status, backref='users')
    
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return '<User %s>' % self.username

'''
class for a logic game
    hands is a list of Hands
    players is a list of strings (corresponding usernames)
    log is a list of strings (actions)
    chat is a list of strings (messages)
    current is the index of the player whose turn it is
    state is the current status:
    - <0 is a bitmask of players who haven't ordered cards
    - 0 means passing
    - 1 means guessing
    - 2 means revealing
    - 3 means calling
    - 4 means over
'''
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    # NOTE: db.JSON does NOT auto-detect in-place mutations the way
    # PickleType did. All mutation paths in app/views.py follow a
    # refresh() -> modify -> insert() pattern, which re-assigns the column
    # and triggers a proper UPDATE. If you add a code path that mutates a
    # persisted Game in place (e.g. game.log.append(...) + commit without
    # refresh/insert), wrap these columns with MutableList/MutableDict or
    # the change will silently not persist.
    hands = db.Column(HandsJSON)
    players = db.Column(db.JSON)
    log = db.Column(db.JSON)
    current = db.Column(db.Integer)
    state = db.Column(db.Integer)
    chat = db.Column(db.JSON)
    notes = db.Column(db.JSON)

    # needs constructor to be able to "refresh" a game
    def __init__(self, name, players, hands=None, log=None, current=None, state=-15, chat=None, notes=None):
        self.name = name

        self.players = players

        self.hands = hands
        if hands is None:
            # randomly shuffles a deck and makes hands
            deck = []
            for val in values:
                for suit in suits:
                    deck.append(Card(val, suit))
            random.shuffle(deck)

            self.hands = []
            for i in range(4):
                self.hands.append(Hand(deck[i*6:i*6+6]))

        self.log = log if log is not None else []
        self.current = current if current is not None else random.randint(0, 3)
        self.state = state
        self.chat = chat if chat is not None else []
        self.notes = notes if notes is not None else {}

    def __str__(self):
        return '<Game %s: %s>' % (self.name, str(self.players))

    # returns the index of a player, or -1 if the player is not in the game
    def index(self, player):
        try:
            return self.players.index(player)
        except ValueError:
            return -1

    # returns a list of 64 items to be passed to the template
    # - a Card means it's someone's card
    # - a string means it's a username
    # - a None means it's empty
    def grid(self, player):
        # rotates hands and players to put the user on the bottom
        number = self.index(player)
        hands = self.hands
        players = self.players[:4]
        if number >= 0:
            hands = hands[number:]+hands[:number]
            players = players[number:]+players[:number]
        players+=self.players[4:]

        # manually puts cards and usernames into the grid
        res = [None]*64
        for i in range(6):
            res[57+i] = hands[0].cards[i]
            if number >= 0:
                res[57+i].private = True
        res[50] = 'R'+players[0]
        for i in range(6):
            res[55-8*i] = hands[1].cards[i]
        res[46] = 'U'+players[1]
        for i in range(6):
            res[6-i] = hands[2].cards[i]
            if number >= 0 and res[6-i].secret:
                res[6-i].private = True
        res[13] = 'L'+players[2]
        for i in range(6):
            res[8+8*i] = hands[3].cards[i]
        res[17] = 'D'+players[3]
        return res
