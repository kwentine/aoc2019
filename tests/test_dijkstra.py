import pytest
from dijkstra import find_shortest_paths, path_to, steps_to

def test_origin_only():
    get_neighbors = lambda x, y: tuple()
    expected = {0: None}
    assert find_shortest_paths(0, get_neighbors) == expected


def test_triangle():
    graph = {
        0: [1, 2],
        2: [3]
    }
    get_neighbors = lambda x,y: graph.get(x, tuple())
    expected = {0: None, 1: 0, 2: 0, 3: 2}
    assert find_shortest_paths(0, get_neighbors) == expected

def test_path_to_origin():
    preds = {0: None}
    assert path_to(0, preds) == [0]

def test_path_to_non_trivial():
    preds = {3: 2, 2: 1, 1: 0, 0: None}
    assert path_to(3, preds) == [0, 1, 2, 3]

def test_steps_to_origin():
    preds = {0: None}
    assert steps_to(0, preds) == []

def test_steps_to_non_trivial():
    UP = (0, 1)
    DOWN = (0, -1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    preds = {
        (1, 0): (1, 1),
        (1, 1): (0, 1),
        (0, 1): (0, 0),
        (0, 0): None
    }
    assert steps_to((1, 0), preds) == [UP, RIGHT, DOWN]
