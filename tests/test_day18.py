import pytest
from day18 import parse_input, get_reacheable_keys, dijkstra, bfs, dfs, dfs4

ex1_1 = """#########
#b.A.@.a#
#########"""

ex1_2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

ex1_3 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

ex1_4 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

ex1_5 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

ex2_1 = """#######
#a.#Cd#
##...##
##.@.##
##...##
#cB#Ab#
#######"""

ex2_3 = """#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############"""


def xtest_parse_input():
    start_x, start_y, n_keys, grid = parse_input(ex1_1)
    assert start_x, start_y == (5, 1)
    assert n_keys == 2
    assert grid[(0, 0)] == "#"
    assert grid[(8, 2)] == "#"

def xtest_reacheable():
    start_x, start_y, n_keys, grid = parse_input(ex1_1)
    reach = get_reacheable_keys(start_x, start_y, "", grid)
    assert reach == set([(7, 1, "a", 2)])

@pytest.mark.parametrize("s,expected", [
    (ex1_1, 8),
    (ex1_2, 86),
    (ex1_3, 132),
    #(ex1_4, 136),
    (ex1_5, 81)
])
def xtest_dijktra(s, expected):
    steps, keys = dijkstra(s)
    assert steps == expected

@pytest.mark.parametrize("s,expected", [
    (ex1_1, 8),
    (ex1_2, 86),
    (ex1_3, 132),
    (ex1_4, 136),
    (ex1_5, 81)
])
def xtest_bfs(s, expected):
    steps, keys = bfs(s)
    assert steps == expected

@pytest.mark.parametrize("s,expected", [
    (ex1_1, 8),
    (ex1_2, 86),
    (ex1_3, 132),
    (ex1_4, 136),
    (ex1_5, 81)
])
def xtest_dfs(s, expected):
    steps = dfs(s)
    assert steps == expected


def test_dfs_4():
    assert dfs4(ex2_3) == 72
