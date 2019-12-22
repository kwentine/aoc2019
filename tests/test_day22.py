import pytest
from day22 import deal_new, cut, deal_incr, apply_ops, parse

@pytest.fixture(scope="module")
def deck():
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def test_deal_new(deck):
    expected = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert deal_new(deck) == expected

def test_cut_positive(deck):
    expected = [int(i) for i in "3 4 5 6 7 8 9 0 1 2".split()]
    assert cut(3, deck) == expected

def test_cut_negative(deck):
    expected = [int(i) for i in "6 7 8 9 0 1 2 3 4 5".split()]
    assert cut(-4, deck) == expected

def test_deal_incr(deck):
    expected = [int(i) for i in "0 7 4 1 8 5 2 9 6 3".split()]
    assert deal_incr(3, deck) == expected

ex1 = """deal with increment 7
deal into new stack
deal into new stack"""

ex2 = """cut 6
deal with increment 7
deal into new stack"""

examples = (
    (ex1, "0 3 6 9 2 5 8 1 4 7"),
    (ex2, "3 0 7 4 1 8 5 2 9 6")
)

@pytest.mark.parametrize("s, expected", examples)
def test_apply_ops(s, expected):
    ops = parse(s)
    res = apply_ops(ops, 10)
    assert " ".join(str(i) for i in res) == expected
