from collections import defaultdict, deque
from typing import Tuple, Dict, Set
import heapq


def read_input():
    with open('data/day18.txt') as f:
        return f.read()
    
def parse_input(s=None):
    grid = defaultdict(str)
    start_x, start_y = 0, 0
    n_keys = 0
    x, y = 0, 0
    if s is None:
        s = read_input()
    for c in s:
        if c == '\n':
            y += 1
            x = 0
            continue
        elif c == "@":
            start_x, start_y = x, y
        elif c.islower():
            n_keys += 1
        grid[(x, y)] = c
        x += 1
    return start_x, start_y, n_keys, grid

def display(grid):
    xmax = max(x for x, _ in grid)
    ymax = max(y for _, y in grid)
    for y in range(ymax + 1):
        for x in range(xmax + 1):
            c = grid[(x, y)]
            if 65 <= ord(c) <= 90:
                color = "\033[1;31m%s\033[m"
            elif 97 <= ord(c) <= 122:
                color = "\033[1;34m%s\033[m"
            elif c == "@":
                color = "\033[1;32m%s\033[m"
            elif c == ".":
                color = "\033[30m%s\033[m"
            else:
                color = "\033[30;40m%s\033[m"
            print(color % grid[(x, y)], end='')
        print()


def bfs(s=None):
    start_x, start_y, tot_keys, grid = parse_input(s or read_input())
    seen = {(start_x, start_y, tuple())}
    todo = deque([(start_x, start_y, "", 0)])
    while todo:
        x, y, keys, d = todo.popleft()
        for (dx, dy) in (
                ( 1,  0),
                (-1,  0),
                ( 0,  1),
                ( 0, -1)
        ):
            nx, ny = x + dx, y + dy
            nd = d + 1
            nkeys = keys
            c = grid[nx, ny]
            if c == "#":
                continue
            if c not in keys:
                if c.isupper() and c.lower() not in keys:
                    continue
                if c.islower():
                    nkeys = keys + c
                    if len(nkeys) == tot_keys:
                        return nd, nkeys
            skeys = tuple(sorted(nkeys))
            if (nx, ny, skeys) not in seen:
                seen.add((nx, ny, skeys))
                todo.append((nx, ny, nkeys, nd))
    print(seen)
    raise AssertionError("Unreacheable!")

# Too slow, involves sorting
def dijkstra(s=None):
    start_x, start_y, tot_keys, grid = parse_input(s or read_input())
    seen = {(start_x, start_y, frozenset())}
    todo = [(0, start_x, start_y, "")]
    while todo:
        d, x, y, keys = heapq.heappop(todo)
        if len(keys) == tot_keys:
            return d, keys
        seen.add((x, y, frozenset(keys)))
        for (nx, ny, nkeys, nd) in get_reacheable_keys(x, y, keys, grid):
            if (nx, ny, frozenset(nkeys)) in seen:
                continue
            heapq.heappush(todo, (nd + d, nx, ny, nkeys))
    raise AssertionError("Unreacheable!")


def dfs(s=None):
    cache = {}
    start_x, start_y, tot_keys, grid = parse_input(s or read_input())
    def _dfs(x, y, keys):
        if len(keys) == tot_keys:
            return 0
        cache_key = (x, y, frozenset(keys))
        if cache_key in cache:
            return cache[(x, y, frozenset(keys))]
        
        reach = get_reacheable_keys(x, y, keys, grid)
        if not reach:
            raise AssertionError("Unreacheable")
        res = []
        for (nx, ny, nkeys, nd) in reach:
            res.append(nd + _dfs(nx, ny, nkeys))
        d = min(res)
        cache[cache_key] = d
        return d
    return _dfs(start_x, start_y, "")
        

def get_reacheable_keys_4(p1, p2, p3, p4, keys, grid):
    for x, y, nkeys, nd in get_reacheable_keys(p1[0], p1[1], keys, grid):
        yield ((x, y), p2, p3, p4, nkeys, nd)
    for x, y, nkeys, nd in get_reacheable_keys(p2[0], p2[1], keys, grid):
        yield (p1, (x, y), p3, p4, nkeys, nd)
    for x, y, nkeys, nd in get_reacheable_keys(p3[0], p3[1], keys, grid):
        yield (p1, p2, (x, y), p4, nkeys, nd)
    for x, y, nkeys, nd in get_reacheable_keys(p4[0], p4[1], keys, grid):
        yield (p1, p2, p3, (x, y), nkeys, nd)

def dfs4(s=None):
    cache = {}
    start_x, start_y, tot_keys, grid = parse_input(s or read_input())
    for (dx, dy) in (
            ( 1,  0),
            (-1,  0),
            ( 0,  1),
            ( 0, -1),
            ( 0,  0)
    ):
        grid[start_x + dx, start_y + dy] = "#"
    display(grid)
    
    def _dfs(p1, p2, p3, p4, keys):
        # breakpoint()
        cache_key = (p1, p2, p3, p4, frozenset(keys))
        if cache_key in cache:
            return cache[cache_key]
        
        reach = tuple(get_reacheable_keys_4(p1, p2, p3, p4, keys, grid))
        if not reach:
            return 0
        res = []
        for (np1, np2, np3, np4, nkeys, nd) in reach:
            res.append(nd + _dfs(np1, np2, np3, np4, nkeys))
        d = min(res)
        cache[cache_key] = d
        return d
    p1 = start_x + 1, start_y + 1
    p2 = start_x + 1, start_y - 1
    p3 = start_x - 1, start_y - 1
    p4 = start_x - 1, start_y + 1
    return _dfs(p1, p2, p3, p4, "")

        
# Definitely ugly too slow, but I tried in a hurry'
def bfs4(s=None):
    objects, grid = parse_input(s or read_input())
    tot_keys = len([c for c in objects if c.islower()])
    in_x, in_y = objects['@']
    for (dx, dy) in (
            ( 1,  0),
            (-1,  0),
            ( 0,  1),
            ( 0, -1),
            ( 0,  0)
    ):
        grid[in_x + dx, in_y + dy] = "#"
    display(grid)
    seen = {(in_x + 1, in_y + 1, in_x + 1, in_y - 1, in_x - 1, in_y + 1, in_x - 1, in_y - 1, tuple())}
    todo = deque([(in_x + 1, in_y + 1, in_x + 1, in_y - 1, in_x - 1, in_y + 1, in_x - 1, in_y - 1, "", 0)])
    while todo:
        x1, y1, x2, y2, x3, y3, x4, y4, keys, d = todo.popleft()
        t = ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
        for i in range(4):
            for (dx, dy) in (
                    ( 1,  0),
                    (-1,  0),
                    ( 0,  1),
                    ( 0, -1)
            ):
                nx, ny = t[i][0] + dx, t[i][1] + dy
                nd = d + 1
                nkeys = keys
                c = grid[nx, ny]
                if c == "#":
                    continue
                if c not in keys:
                    if c.isupper() and c.lower() not in keys:
                        continue
                    if c.islower():
                        nkeys = keys + c
                        if len(nkeys) == tot_keys:
                            return nd, nkeys
                skeys = tuple(sorted(nkeys))
                l = list(t)
                l[i] = (nx, ny)
                tl = tuple(x for y in l for x in y) + (tuple(skeys) if skeys else ((),))
                if tl not in seen:
                    seen.add(tl)
                    todo.append(tuple(x for y in l for x in y) + (nkeys, nd))
    print(seen)
    raise AssertionError("Unreacheable!")


def get_reacheable_keys(x: int, y: int, keys: str, grid: Dict[str, str]) -> Set[Tuple[int, int, str, int]]:
    """Keys immediatly reacheable from (x, y)"""
    visited = set()
    todo = deque([(x, y, 0)])
    reach = set()
    while todo:
        x, y, d = todo.popleft()
        for (dx, dy) in (
                ( 1,  0),
                (-1,  0),
                ( 0,  1),
                ( 0, -1)
        ):
            
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited:
                continue
            nd = d + 1
            c = grid[nx, ny]
            # Wall
            if c == "#":
                continue
            # Closed door
            if c.isupper() and c.lower() not in keys:
                continue
            # New key
            if c.islower() and c not in keys:
                reach.add((nx, ny, keys + c, d + 1))
                continue
            visited.add((nx, ny))
            todo.append((nx, ny, nd))
    return reach

if __name__ == "__main__":
    print(f"Keys collected in {dfs4()} steps.")
