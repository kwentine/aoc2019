import pytest
from day22 import (deal_new, cut, deal_incr, compose, shuffle, parse,
                   shuffle_from_spec, compose_many)

@pytest.fixture(scope="module")
def deck():
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def test_deal_new(deck):
    assert deal_new(deck) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

def test_cut_positive(deck):
    assert cut(3, deck) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

def test_cut_negative(deck):
    assert cut(-4, deck) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    
def test_deal_incr(deck):
    assert deal_incr(3, deck) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]

@pytest.mark.parametrize("a,b,c,d",(
    (-1, -1, 3, 0),
    (-1, -1, 1, -3),
    (1, -3, 3, 0)
    
))
def test_compose(deck, a, b, c, d):
    x, y = compose(a, b, c, d)
    assert shuffle(c, d, deck=shuffle(a, b, deck=deck)) == shuffle(x, y, deck=deck)

@pytest.mark.parametrize("a,b,c,d",(
    (-1, -1, 3, 0),
    (-1, -1, 1, -3),
    (1, -3, 3, 0)
    
))
def test_compose_many(deck, a, b, c, d):
    x, y = compose_many([(a, b), (c, d)], 10)
    assert shuffle(c, d, deck=shuffle(a, b, deck=deck)) == shuffle(x, y, deck=deck)
    
ex1 = """deal with increment 7
deal into new stack
deal into new stack"""

ex2 = """cut 6
deal with increment 7
deal into new stack"""

examples = (
    (ex1, [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]),
    (ex2, [3, 0, 7, 4, 1, 8, 5, 2, 9, 6])
)

@pytest.mark.parametrize("s, expected", examples)
def test_shuffle_from_spec(s, expected):
    assert shuffle_from_spec(s, 10) == expected
