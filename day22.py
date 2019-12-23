"""Day 22: Slam Shuffle"""
from functools import partial
from utils import get_input

def parse(s):
    """op -> (a, b) where op : x -> a * x + b"""
    res = []
    for l in s.splitlines():
        descr, arg = l.rsplit(' ', 1)
        if "new" in descr:
            op = (-1, -1)
        elif "increment" in descr:
            op = (int(arg), 0)
        elif descr == "cut":
            op = (1, -1 * int(arg))
        else:
            AssertionError(f"Unknown technique: {l}")
        res.append(op)
    return res


def shuffle(a, b, *, deck=None, deck_size=None):
    assert (deck is not None or deck_size is not None)
    n = deck_size if deck_size is not None else len(deck)
    deck = deck if deck is not None else list(range(deck_size))
    res = [0] * n
    for i in range(n):
        res[(i * a + b ) % n] = deck[i]
    return res

deal_new = lambda deck: shuffle(-1, -1, deck=deck)
deal_incr = lambda k, deck: shuffle(k, 0, deck=deck)
cut = lambda k, deck: shuffle(1, -k, deck=deck)

compose = lambda a, b, c, d: (a * c, b * c + d)
        
def compose_many(ops, deck_size):
    """Sum of operations as x -> a * x + b [len(deck)]"""
    a, b = 1, 0
    for (c, d) in ops:
        a, b = compose(a, b, c, d)
    return a % deck_size, b % deck_size

def shuffle_from_spec(spec, deck_size):
    ops = parse(spec)
    a, b = compose_many(ops, deck_size)
    return shuffle(a, b, deck_size=deck_size)
    
def level1():
    ops = get_input(22, parse)
    deck_size = 10007
    (a, b) = compose_many(ops, deck_size)
    return (a * 2019 + b) % deck_size

if __name__ == "__main__":
    print(f"{level1()}")
            
    
