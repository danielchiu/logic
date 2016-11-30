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
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit
        self.name = val+suit
        self.private = False
        self.flipped = False 
        self.secret = False

    def __str__(self):
        if self.flipped:
            return self.name
        else:
            return '_'+self.suit

'''
class for a player's hand
sorts cards by value, breaking ties by original order (stable)
'''
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort(key = lambda card: values.index(card.val)) 

    def __str__(self):
        return ' '.join(map(str,self.cards))
