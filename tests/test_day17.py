import pytest
from day17 import forward, parse_grid, DIRECTIONS, generate_instructions

def test_parse_grid():
    s = """\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
"""
    x, y, dx, dy, h, w, grid = parse_grid(s)
    assert grid[y][x] == '^'
    assert h == len(grid)
    assert w == len(grid[0])
    assert DIRECTIONS['^'] == (dx, dy)


def test_forward():
    s = """\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...^..
"""
    x, y, dx, dy, h, w, grid = parse_grid(s)
    assert forward(x, y, dx, dy, grid) == 4
    assert forward(x, y, 1, 0, grid) == 0


def test_generate_instructions():
    s = """\
..#..........
..#..........
#######...###
#.#...#...#.#
#############
..#...#...#..
..#####...<..
"""
    x, y, dx, dy, h, w, grid = parse_grid(s)
    instr = "".join(generate_instructions(x, y, dx, dy, grid))
    expected = 'R4R2R2R12R2R6R4R4R6'
    assert instr == expected
