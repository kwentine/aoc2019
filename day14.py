from collections import defaultdict
import math


def read_input(day):
    with open(f"data/day{day:02d}.txt") as f:
        return f.read()


def parse_line(l):
    reactives, product = l.strip().split("=>")
    reactives = [parse_term(r) for r in reactives.split(",")]
    chem, qty = parse_term(product)
    return (chem, qty, reactives)


def parse_term(s):
    qty, chem = s.split()
    return (chem, int(qty))


def parse_input(s):
    units = {}
    requires = {}
    reactions = [parse_line(l) for l in s.split("\n") if l]
    for (chemical, qty, reactives) in reactions:
        units[chemical] = qty
        requires[chemical] = dict(reactives)
    return units, requires


def solve(units, reactions):

    stock = defaultdict(int)
    consumed = defaultdict(int)

    def consume(chem, k):
        """Consume `k` units of chemical `chem`"""
        if chem == "ORE":
            pass

        elif stock[chem] >= k:
            stock[chem] -= k

        else:
            missing = k - stock[chem]
            reactions_needed = math.ceil(missing / units[chem])
            for (react, qty) in reactions[chem].items():
                consume(react, reactions_needed * qty)

            stock[chem] = stock[chem] + reactions_needed * units[chem] - k

        consumed[chem] += k

    consume("FUEL", 1)
    return consumed["ORE"]

def solve2(units, reactions, supply=0):

    stock = defaultdict(int)
    consumed = defaultdict(int)
    
    def consume(chem, k):
        nonlocal supply
        """Consume `k` units of chemical `chem`"""
        if chem == "ORE":
            if k > supply:
                raise ValueError("Supplies exhausted")
            supply -= k

        elif stock[chem] >= k:
            stock[chem] -= k

        else:
            missing = k - stock[chem]
            reactions_needed = math.ceil(missing / units[chem])
            for (react, qty) in reactions[chem].items():
                consume(react, reactions_needed * qty)

            stock[chem] = stock[chem] + reactions_needed * units[chem] - k

        consumed[chem] += k

    chunk = 1000
    while chunk:
        saved_supply = supply
        saved_stock = stock.copy()
        saved_consumed = consumed.copy()
        try:
            consume("FUEL", chunk)
        except ValueError:
            supply = saved_supply
            stock.update(saved_stock)
            consumed.update(saved_consumed)
            chunk -= 1
    return consumed["FUEL"]

def level1():
    units, requires = parse_input(read_input(14))
    print(solve(units, requires))

def level2():
    units, requires = parse_input(read_input(14))
    print(solve2(units, requires, supply=10 ** 12))


level2()
