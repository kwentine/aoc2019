from utils import get_input, display
from collections import defaultdict

DAY = 20

def parse(s: str) -> dict:
    grid = defaultdict(lambda: ' ')
    x, y = 0, 0
    for c in s:
        if c == '\n':
            y += 1
            x = 0
            continue
        grid[x, y] = c
        x += 1
    return grid

cmap = [
    (lambda c: c.isupper(), "\033[1;31m{}\033[m"),
    (".", "\033[47m \033[m"),
    ("#", "\033[40m \033[m")
]

def neighbors(x, y):
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        yield x + dx, y + dy


def get_neighbors(self):
    pass


def parse_grid(grid):
    portals = defaultdict(list)
    letters = [x for x in grid.items() if x[1].isupper()]
    start = None
    end = None
    for ((x, y), c) in letters:
        entrance = None
        label = None
        for pt in neighbors(x, y):
            n = grid[pt]
            if n == '.':
                entrance = pt
            if n.isupper():
                label = "".join(sorted(c + n))
        if entrance is None:
            continue
        if label == "AA":
            start = entrance
            continue
        if label == "ZZ":
            end = entrance
            continue
        portals[label].append(entrance)
    assert start is not None
    assert end is not None
    assert all(len(l) == 2 for (_, l) in portals.items())
    portal_map = {}
    for (_, l) in portals.items():
        portal_map[l[0]] = l[1]
        portal_map[l[1]] = l[0]
    return start, end, portal_map
    
            

# if __name__ == "__main__":
#     grid = get_input(DAY, parse, strip=False)
#     display(grid, cmap)

                
    
    
