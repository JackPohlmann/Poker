'''
deck

a 52-card deck

initializes all cards.
capable of shuffling and dealing
'''

import numpy as np
import random

from card import Card

class Deck:
    def __init__(self):
        self.deck = []
        self.dead = []
        self.remake()

    def remake(self):
        self.deck.clear()
        self.dead.clear()
        for suit in Card.suits:
            for value in Card.values:
                self.deck.append(Card(value, suit))

    def shuffle(self):
        self.remake()
        random.shuffle(self.deck)

    def deal(self, n=1):
        out = []
        for ii in range(n):
            out.append(self.deck.pop())
        return out
    
    def muck(self, n=1):
        for ii in range(n):
            self.dead.append(self.deck.pop())
