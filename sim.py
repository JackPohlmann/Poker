'''
main

runs a simulated poker hand
does not simulate betting

can run tests by supplying the command line argument 'test'
'''

import sys

from card import Card
import game


'''
TODO: simulate GTO betting
'''

def test_sets_pairs():
    t = game.Game(6, 1500)
    def deal():
        t.seat_cards.append([Card(14, 'h'), Card(14, 's')])
        t.seat_cards.append([Card(5, 'h'), Card(4, 'h')])

        t.seat_cards.append([Card(3, 'c'), Card(2, 'h')])
        t.seat_cards.append([Card(3, 'h'), Card(5, 'h')])

        t.seat_cards.append([Card(9, 'h'), Card(12, 's')])
        t.seat_cards.append([Card(13, 'h'), Card(12, 'h')])
        t.board = [Card(4, 's'), Card(14, 'c'), Card(13, 's'), Card(12, 'c'), Card(6, 'd')]
    t.deal = deal
    t.play()

def test_royal_flush():
    t = game.Game(6, 1500)
    def deal():
        t.seat_cards.append([Card(14, 'h'), Card(13, 'h')])
        t.seat_cards.append([Card(11, 'c'), Card(11, 's')])
        t.seat_cards.append([Card(5, 'h'), Card(6, 'h')])
        t.seat_cards.append([Card(9, 'c'), Card(8, 'c')])
        t.seat_cards.append([Card(9, 'h'), Card(8, 'h')])
        t.seat_cards.append([Card(12, 's'), Card(12, 'd')])
        t.board = [Card(12, 'h'), Card(11, 'h'), Card(10, 'h'), Card(12, 'c'), Card(10, 'd')]
    t.deal = deal
    t.play()


if __name__ == "__main__":
    if 'test' in sys.argv:
        test_sets_pairs()
        print()
        test_royal_flush()
    else:
        he = game.HoldEm()
        he.play()