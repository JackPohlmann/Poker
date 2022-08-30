'''
game

abstract poker variant
'''

from card import Card
from deck import Deck
from hand import Hand

class Game:
    def __init__(self, hands, stack):
        self.count = hands
        self.seat_cards = []
        self.seat_map = {}
        self.hands = []
        self.stacks = []
        self.deck = Deck()
        self.board = []
        self.deck.shuffle()

    def deal(self):
        pass

    def flop(self):
        pass

    def turn(self):
        pass

    def river(self):
        pass

    def eval(self):
        for i in range(len(self.seat_cards)):
            seat = self.seat_cards[i]
            hand = Hand(seat + self.board)
            self.hands.append(hand)
            self.seat_map[hand] = i
        self.hands.sort(reverse=True, key=lambda h: h.score)
        return self.seat_map[self.hands[0]]

    def play(self):
        self.reset()
        self.deal()
        for i in range(len(self.seat_cards)):
            seat_hand = ''
            for c in self.seat_cards[i]:
                seat_hand += str(c) + ' '
            print(f"{i}: {seat_hand}")

        print()
        self.flop()
        self.turn()
        self.river()
        winner = self.eval()
        self.display()
        print()
        print('='*(len(Hand.header) + 6))
        print("Seat" + ' '*2 + Hand.header)
        print('='*(len(Hand.header) + 6))
        for hand in self.hands:
            #print(f"{self.seat_map[hand]}: {hand.title}")
            print("{:4}: {}".format(self.seat_map[hand], str(hand)))
        print('='*(len(Hand.header) + 6))
        return

    def display(self):
        out = '\t'
        for c in self.board:
            out += str(c) + ' '
        print(out)
    
    def display_seat_cards(self):
        out = ''
        for h in self.seat_cards:
            for c in h:
                out += str(c)
            out += ' '
        print(out)

    def reset(self):
        self.seat_cards.clear()
        self.seat_map.clear()
        self.board.clear()
        self.deck.shuffle()

    def peek(self, seat):
        out = ''
        for c in self.seat_cards[seat]:
            out += str(c)
        return out


class HoldEm(Game):
    '''
    implementation of Texas Hold Em
    '''
    def __init__(self, hands=6, stack=1500):
        super().__init__(hands, stack)

    def deal(self):
        for i in range(self.count):
            self.seat_cards.append(self.deck.deal(2))

    def flop(self):
        self.deck.muck(3)
        self.board += self.deck.deal(3)

    def turn(self):
        self.deck.muck()
        self.board += self.deck.deal()

    def river(self):
        self.deck.muck()
        self.board += self.deck.deal()
