import random

values = ['A','2','3','4','5','6','7','8','9','T','J','Q']
suits = ['H','S']

''' 
class for a card in a player's hand 
    private = visible to self
    flipped = visible to everyone
    secret = visible to self and partner
'''
class Card:
    def __init__(self, val, suit, flipped=False, secret=False, private=False):
        self.val = val
        self.suit = suit
        self.name = val+suit
        self.private = private
        self.flipped = flipped
        self.secret = secret

    def __str__(self):
        if self.flipped:
            return self.name
        else:
            return '_'+self.suit

    def to_dict(self):
        return {
            'val': self.val,
            'suit': self.suit,
            'flipped': self.flipped,
            'secret': self.secret,
            'private': self.private,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['val'], d['suit'], d.get('flipped', False),
                   d.get('secret', False), d.get('private', False))

'''
class for a player's hand
sorts cards by value, breaking ties by original order (stable)
'''
class Hand:
    def __init__(self, cards, sort=True):
        self.cards = cards
        if sort:
            self.cards.sort(key = lambda card: values.index(card.val))

    def __str__(self):
        return ' '.join(map(str,self.cards))

    def to_dict(self):
        return [card.to_dict() for card in self.cards]

    @classmethod
    def from_dict(cls, card_list):
        cards = [Card.from_dict(d) for d in card_list]
        return cls(cards, sort=False)
