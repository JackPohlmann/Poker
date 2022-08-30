'''
card

an individual card

note that face cards are designated using their value, not their title.
ie. A = 14, K = 13, Q = 12, J = 11
'''

import numpy as np

class Card:
    values = np.arange(13) + 2
    suits = ['s', 'c', 'd', 'h']
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        if self.value == 10:
            v = 'T'
        elif self.value == 11:
            v = 'J'
        elif self.value == 12:
            v = 'Q'
        elif self.value == 13:
            v = 'K'
        elif self.value == 14:
            v = 'A'
        else:
            v = str(self.value)
        return v + self.suit