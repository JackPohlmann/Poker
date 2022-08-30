'''
hand

evaluates a poker hand.
hands are scored by generating a single, comparable value.

there are 9 potential poker hands:
1) straight flush
2) 4 of a kind
3) full house
4) flush
5) straight
6) 3 of a kind
7) 2 pair
8) pair
9) high card

there are 13 cards, but claim there are 14 since Aces can be low or high:
14) Ace
13) King
12) Queen
11) Jack
10) 10
9) 9
8) 8
7) 7
6) 6
5) 5
4) 4
3) 3
2) 2
1) Ace (low)

hand valuation generates a value using base 14:
let H = hand rank
let C = card rank
let V = valuation
thus:
V = C * 14 ^ H

ties are broken by summing the hand's card values:
let T = tie breaker
T = sum(C_n * 14 ^ (5 - n))

'''

from card import Card

def _fill_by_suit(cards):
    out = {}
    for suit in Card.suits:
        out[suit] = []
    for card in cards:
        out[card.suit].append(card)
    return out

def _fill_by_value(cards):
    out = {}
    for value in Card.values:
        out[value] = []
    for card in cards:
        out[card.value].append(card)
    return out

class Hand:
    header = "{:<30}{:^20}{:>17}".format("Hand", "Cards", "Score")
    def __init__(self, cards):
        self.cards = cards
        self.hand = []
        self.title = ''

        self.cards_by_suit = _fill_by_suit(cards)
        self.cards_by_value = _fill_by_value(cards)

        self.score = self._eval()

    def __str__(self):
        out = "{:30}".format(self.title)
        out += " [ "
        for c in self.hand:
            out += str(c) + ' '
        out += "] "
        out += f"{self.score:>17.5f}"
        return out

    def _eval(self):
        score = 0.0
        score += self._straight_flush()
        score += self._4_oak()
        score += self._full_house()
        score += self._flush()
        score += self._straight()
        score += self._3_oak()
        score += self._2_pair()
        score += self._high_card() 
        return score

    def _straight_flush(self):
        # 14 ^ 8
        # test if there's a flush
        suit = 0
        for s in Card.suits:
            if len(self.cards_by_suit[s]) >= 5:
                suit = s
        if suit == 0:
            return 0
        hand = []
        fbv = _fill_by_value(self.cards_by_suit[suit])
        start = 0
        count = 0
        for v in reversed(Card.values):
            if len(fbv[v]) > 0:
                if count == 0:
                    start = v
                count += 1
                if count == 5:
                    # found a straight!
                    for i in reversed(range(start - 4, start + 1)):
                        self.hand.append(fbv[i][0])
                    if start == 14:
                        self.title += "Royal Flush!"
                    else:
                        self.title += f"Straight Flush {str(self.hand[0])[0]} high"
                    return float(start) * (14 ** 8)
            else:
                count = 0
        return 0
        
    def _4_oak(self):
        # 14 ^ 7
        if len(self.hand) > 1:
            return 0
        for v in reversed(Card.values):
            if len(self.cards_by_value[v]) == 4:
                self.hand += self.cards_by_value[v]
                self.title += f"Four of a Kind {str(self.hand[0])[0]}s"
                return float(v) * (14 ** 7)
        return 0

    def _full_house(self):
        # 14 ^ 6
        if len(self.hand) > 0:
            return 0
        for v in reversed(Card.values):
            if len(self.cards_by_value[v]) == 3:
                for v2 in reversed(Card.values):
                    if v2 == v:
                        continue
                    if len(self.cards_by_value[v2]) >= 2:
                        self.hand += self.cards_by_value[v] + self.cards_by_value[v2][:2]
                        self.title += f"Full House {str(self.hand[0])[0]}s full of {str(self.cards_by_value[v2][0])[0]}s"
                        return float(v) * (14 ** 6) + float(v2) * (14 ** 2)
        return 0

    def _flush(self):
        # 14 ^ 5
        if len(self.hand) > 0:
            return 0
        suit = 0
        for s in Card.suits:
            if len(self.cards_by_suit[s]) >= 5:
                suit = s
        if suit == 0:
            return 0
        fbv = sorted(self.cards_by_suit[suit], reverse=True, key=lambda c: c.value)
        self.hand += fbv[:5]
        self.title += f"Flush {str(self.hand[0])[0]} high"
        return float(self.hand[0].value) * (14 ** 5)

    def _straight(self):
        # 14 ^ 4
        if len(self.hand) > 0:
            return 0
        start = 0
        count = 0
        for v in reversed(Card.values):
            if len(self.cards_by_value[v]) > 0:
                if count == 0:
                    start = v
                count += 1
                if count == 5:
                    # found a straight!
                    for i in reversed(range(start - 4, start + 1)):
                        self.hand.append(self.cards_by_value[i][0])
                    self.title += f"Straight {str(self.hand[0])[0]} high"
                    return float(start) * (14 ** 4)
            else:
                count = 0
        return 0

    def _3_oak(self):
        # 14 ^ 3
        if len(self.hand) > 2:
            return 0
        for v in reversed(Card.values):
            if len(self.cards_by_value[v]) == 3:
                self.hand += self.cards_by_value[v]
                self.title += f"Three of a Kind {str(self.hand[0])[0]}s"
                return float(v) * (14 ** 3)
        return 0

    def _2_pair(self):
        # 14 ^ 2
        if len(self.hand) > 3:
            return 0
        for v in reversed(Card.values):
            if len(self.cards_by_value[v]) == 2:
                for v2 in reversed(Card.values):
                    if v2 == v:
                        continue
                    if len(self.cards_by_value[v2]) == 2:
                        self.hand += self.cards_by_value[v] + self.cards_by_value[v2][:2]
                        self.title += f"Two Pair {str(self.hand[0])[0]}s and {str(self.cards_by_value[v2][0])[0]}s"
                        return float(v) * (14 ** 2) + float(v2) * (14 ** 1)
                self.hand += self.cards_by_value[v]
                self.title += f"Pair {str(self.hand[0])[0]}s"
                return float(v) * (14 ** 2)
        return 0

    def _high_card(self):
        # 14 ^ 0
        if len(self.hand) > 4:
            return 0
        if len(self.hand) > 0:
            self.title += ", "
        out = 0
        exp = 0
        hc = len(self.hand)
        cards = sorted(self.cards, key=lambda c: c.value)
        while len(self.hand) < 5:
            while cards[-1] in self.hand:
                cards.pop()
            self.hand.append(cards.pop())
            out += self.hand[-1].value * 14 ** exp
            exp -= 1
        self.title += f"{str(self.hand[hc])[0]} high"
        return float(out)
