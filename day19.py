from utils import get_input
from itertools import product
from collections import defaultdict
from day05 import run_async

DAY = 11

def parse_input(s):
    return [int(x) for x in s.split(',')]

def is_pulled(x, y, prog):
    machine = run_async(prog)
    machine.send(None)
    machine.send(x)
    return machine.send(y)

def level1():
    prog = get_input(19, parse_input)
    return sum(is_pulled(x, y, prog) for (x, y) in product(range(size), range(size)))

def draw_beam(size=50):
    prog = get_input(19, parse_input)
    grid = defaultdict(lambda: '.')
    for (x, y) in product(range(50), range(50)):
        if is_pulled(x, y, prog):
            grid[(x, y)] = '#'
    display(grid, xmax=size, ymax=size)

def display(grid, xmax=None, ymax=None):
    xmax = xmax or max(x for x, _ in grid)
    ymax = xmax or max(y for _, y in grid)
    for y in range(ymax + 1):
        for x in range(xmax + 1):
            c = grid[(x, y)]
            if c == "#":
                color = "\033[1;32m%s\033[m"
            elif c == ".":
                color = "\033[30m%s\033[m"
            print(color % c, end='')
        print()



# if __name__ == "__main__":
#     print(f"Tractor affects {level1()} points.")
    
