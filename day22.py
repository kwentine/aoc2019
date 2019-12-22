"""Day 22: Slam Shuffle"""
from functools import partial
from utils import get_input

def deal_new(deck):
    return list(reversed(deck))

def cut(n, deck):
    assert abs(n) < len(deck)
    if n < 0:
        n = len(deck) + n
    return deck[n:] + deck[:n]

def deal_incr(step, deck):
    l = len(deck)
    res = [0] * l
    for i in range(len(deck)):
        res[(i * step) % l] = deck[i]
    return res

def parse(s):
    res = []
    for l in s.splitlines():
        name, arg = l.rsplit(' ', 1)
        if "new" in name:
            res.append(deal_new)
        elif "increment" in name:
            res.append(partial(deal_incr, int(arg)))
        elif name == "cut":
            res.append(partial(cut, int(arg)))
        else:
            raise ValueError(f"Unknown technique: '{name}'")
    return res                    
    

def apply_ops(ops, deck_size):
    deck = list(range(deck_size))
    for op in ops:
        deck = op(deck)
    return deck
        
def level1():
    ops = get_input(22, parse)
    deck = apply_ops(ops, 10007)
    for (i, card) in enumerate(deck):
        if card == 2019: return i
    else:
        raise AssertionError("Unreacheable")

if __name__ == "__main__":
    print(f"{level1()}")
            
    
