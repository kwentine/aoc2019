from utils import get_input, display
from collections import defaultdict
import pdb
import heapq
DAY = 20

def parse(s: str) -> dict:
    grid = defaultdict(lambda: '')
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
                lx, ly = pt
                if lx == x:
                    label = n + c if ly < y else c + n
                elif ly == y:
                    label = n + c if lx < x else c + n
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
    
# Yet another Dijkstra
def dist(start, end, portals, grid):
    seen = set()
    todo = [(0, start)]
    while todo:
        d, pos = heapq.heappop(todo)
        if pos == end: return d
        seen.add(pos)
        for next_pos in neighbors(*pos):
            if next_pos in seen: continue
            c = grid[next_pos]
            if c == "#":
                continue
            if c.isupper():
                if pos == start:
                    continue
                next_pos = portals[pos]
            heapq.heappush(todo, (d + 1, next_pos))
    raise AssertionError("Unreacheable")

def parse_grid_2(grid):
    """Parse the grid portals and start/end for level 2"""
    portals = defaultdict(list)
    letters = [x for x in grid.items() if x[1].isupper()]
    start = None
    end = None
    for ((x, y), c) in letters:
        entrance = None
        label = None
        for other in neighbors(x, y):
            n = grid[other]
            if n == '.':
                entrance = other
            if n.isupper():
                other_x, other_y = other
                # Vertical portal
                if other_x == x:
                    if other_y < y:
                        label = n + c
                        # Outer edge, level increases when appering here
                        if not grid[other_x, other_y - 1]:
                            level = 1
                        else:
                            level = -1
                    else:
                        label = c + n
                        if not grid[other_x, other_y + 1]:
                            level = 1
                        else:
                            level = -1
                if other_y == y:
                    if other_x < x:
                        label = n + c
                        # Outer edge, level increases when appering here
                        if not grid[other_x - 1, other_y]:
                            level = 1
                        else:
                            level = -1
                    else:
                        label = c + n
                        if not grid[other_x + 1, other_y]:
                            level = 1
                        else:
                            level = -1
        if entrance is None:
            continue
        if label == "AA":
            start = entrance
            continue
        if label == "ZZ":
            end = entrance
            continue
        portals[label].append((entrance, level))
    assert start is not None
    assert end is not None
    assert all(len(l) == 2 for (_, l) in portals.items())
    portal_map = {}
    for (_, l) in portals.items():
        portal_map[l[0][0]] = l[1]
        portal_map[l[1][0]] = l[0]
    return start, end, portal_map

def dist_2(start, end, portals, grid):
    seen = set()
    todo = [(0, 0, start)]
    while todo:
        d, level, pos = heapq.heappop(todo)
        if (pos, level) in seen: continue
        assert level >= 0, f"Negative level {level}"
        assert grid[pos] not in {'', ' ', '#'}
        if pos == end and not level: return d
        assert (pos, level) not in seen
        seen.add((pos, level))
        assert (pos, level) in seen
        for new_pos in neighbors(*pos):
            new_level = level
            new_dist = d + 1
            # At level > 0, start and end are walls
            if new_pos == start: continue
            if new_pos == end and level: continue
            # At level 0 portals are walls
            if new_pos in portals and portals[new_pos][1] == -1 and new_level == 0: continue
            c = grid[new_pos]
            if c == "#": continue
            # We are trying to cross a portal
            if c.isupper():
                if pos == start: continue
                new_pos, incr = portals[pos]
                new_level += incr
            if (new_pos, new_level) in seen: continue
            assert (new_level, new_pos) not in seen
            heapq.heappush(todo, (new_dist, new_level, new_pos))
    raise AssertionError("Unreacheable")


def level1():
    grid = get_input(20, parse, strip=False)
    display(grid, cmap)
    start, end, portals = parse_grid(grid)
    return dist(start, end, portals, grid)

def level2():
    grid = get_input(20, parse, strip=False)
    start, end, portals = parse_grid_2(grid)
    return dist_2(start, end, portals, grid)

if __name__ == "__main__":
    print(level2())


                
    
    
