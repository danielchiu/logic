import random

values = ['A','2','3','4','5','6','7','8','9','T','J','Q']
suits = ['H','S']

class Card:
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit
        self.name = val+suit
        self.hidden = True

    def __str__(self):
        if self.hidden:
            return '_'+self.suit
        else:
            return self.name

    def flip(self):
        self.hidden = False

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.cards.sort(key = lambda card: values.index(card.val)) 

    def __str__(self):
        return ' '.join(map(str,self.cards))

class Game:
    def __init__(self):
        self.deck = []
        for val in values:
            for suit in suits:
                self.deck.append(Card(val,suit))
        random.shuffle(self.deck)

        self.hands = []
        for i in range(4):
            self.hands.append(Hand(self.deck[i*6:i*6+6]))

        self.turn = random.randInt(1,4)

    def __str__(self):
        return '\n'.join(map(str,self.hands))

    def flip(self, hand, card):
        self.hands[hand].cards[card].flip()

    

master = Game()
print(master)
while True:
    a,b = map(int,input().split())
    master.flip(a,b)
    print(master)
