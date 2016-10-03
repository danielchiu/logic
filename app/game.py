import random

values = ['A','2','3','4','5','6','7','8','9','T','J','Q']
suits = ['H','S']

class Card:
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit
        self.name = val+suit
        self.flipped = True if random.randint(1,6)==1 else False # TODO actually do something legit here

    def __str__(self):
        if self.flipped:
            return self.name
        else:
            return '_'+self.suit

    def flip(self):
        self.flipped = True

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort(key = lambda card: values.index(card.val)) 

    def __str__(self):
        return ' '.join(map(str,self.cards))
