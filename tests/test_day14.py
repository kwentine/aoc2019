import pytest
import sys
from day14 import parse_input, solve, solve2

def test_parse_line():
    pass

ex_1 = """\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
"""

ex_2 = """\
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

ex_3 = """\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

ex_4 = """\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""

ex_5 = """\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""

def test_parse_input():
    units = dict(A=10, B=1, C=1, D=1, E=1, FUEL=1)
    requires = {
        'A': {'ORE': 10},
        'B': {'ORE': 1},
        'C': {'A': 7, 'B': 1},
        'D': {'A': 7, 'C': 1},
        'E': {'A': 7, 'D': 1},
        'FUEL': {'A': 7, 'E': 1},
    }
    assert parse_input(ex_1) == (units, requires)


def test_solve_direct_reaction():
    units = dict(FUEL=1)
    requires = {'FUEL': {'ORE': 1}}
    assert solve(units, requires) == 1

def test_solve_indirect_reaction():
    s = """\
1 ORE => 1 A
1 A => 1 FUEL
"""
    units, reactions = parse_input(s)
    assert solve(units, reactions) == 1

def test_solve_indirect_reaction_needed_twice():
    s = """\
1 ORE => 1 A
2 A => 1 FUEL
"""
    units, reactions = parse_input(s)
    assert solve(units, reactions) == 2

def test_solve_indirect_reaction_2():
    s = """\
1 ORE => 1 A
5 ORE => 1 B 
2 A, 1 B => 1 FUEL
"""
    units, reactions = parse_input(s)
    assert solve(units, reactions) == 7

def test_solve_indirect_reaction_3():
    s = """\
1 ORE => 1 A
2 A  => 1 B 
3 B  => 1 FUEL
"""
    units, reactions = parse_input(s)
    assert solve(units, reactions) == 6

    

def test_example_1():
    units, reactions = parse_input(ex_1)
    assert solve(units, reactions) == 31
    

@pytest.mark.parametrize('s, expected', [
    (ex_1, 31),
    (ex_2, 165),
    (ex_3, 13312),
    (ex_4, 180697),
    (ex_5, 2210736)
]) 
def test_solve(s, expected):
    units, reactions = parse_input(s)
    assert solve(units, reactions) == expected 

def test_solve2():
    units, reactions = parse_input(ex_3)
    assert solve2(units, reactions, supply=10**12) == 82892753
