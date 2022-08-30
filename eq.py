'''
eq

first-order poker math
'''

import math

def out_odds_flop(outs):
    A = outs / 50
    B = (1 - A) * outs / 49
    C = (1 - B) * outs / 48
    return A + B + C

def out_odds_flop_turn(outs):
    return outs / 47

def out_odds_turn_river(outs):
    return outs / 46

def out_odds_flop_river(outs):
    B = out_odds_flop_turn(outs)
    C = (1 - B) * out_odds_turn_river(outs)
    return B + C

def out_odds_preflop(outs):
    A = out_odds_flop(outs)
    B = (1 - A) * out_odds_flop_turn(outs)
    C = (1 - B) * out_odds_turn_river(outs)
    return A + B + C
    

def odds(nouts, ndraws, nremaining):
    prod = 1
    for i in range(ndraws):
        prod *= (nremaining - nouts - i) / (nremaining - i)
    return 1 - prod

def pct_odds(nouts, ndraws, nremaining):
    return 100 * odds(nouts, ndraws, nremaining)

FLOP_SET = odds(2, 3, 50)

def req_pot_odds(raise_pct):
    def _req_pot_odds(pct, nplayers):
        equity = pct / 100
        req_pot_frac = (raise_pct / equity) - (1 + nplayers * raise_pct)
        return 100 * max(0, req_pot_frac)
    return _req_pot_odds