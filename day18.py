import heapq
from collections import defaultdict


ex1 = """#########
#b.A.@.a#
#########"""

ex2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################"""

ex3 = """########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################"""

ex4 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################"""

ex5 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################"""

def read_input():
    with open('data/day18.txt') as f:
        return f.read()
    
def parse_input(s=None):
    grid = defaultdict(str)
    items = {}
    entrance = 0, 0
    x, y = 0, 0
    if s is None:
        s = read_input()
    for c in s:
        if c == '\n':
            y += 1
            x = 0
            continue
        if c not in '.#':
            items[c] = x, y
        grid[(x, y)] = c
        x += 1
    return items, grid

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


def find_closests(origin, grid):
    visited = set()
    todo = deque([(0, origin)])
    closests = set()
    dmin = 1000
    while todo:
        d, cur = todo.popleft()
        visited.add(cur)
        if d > dmin:
            return closests
        if grid[cur].islower():
            closests.add((grid[cur], cur, d))
            dmin = d
        else:
            for x in get_neighbors(cur, grid):
                if x not in visited:
                    todo.append((d + 1, x))
    return closests


def greedy():
    objects, grid = parse_input()
    n_keys = 0
    cost = 0
    loc = objects['@']
    sym = '@'
    while n_keys < 26:
        grid[loc] = '.'
        grid[objects[sym.upper()]] = '.'
        candidates = find_closests(loc, grid)
        sym, loc, dist = candidates.pop()
        print(f'{sym} ({dist})')
        n_keys += 1
        cost += dist
    return cost


def get_neighbors(cur, grid):
    """Accessible neighbors"""
    x, y = cur
    for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if not grid[nx, ny]: continue
        if grid[nx, ny] == '.' or grid[nx, ny].islower():
            yield (nx, ny)

            
def brute_force(objects, grid, sym='@'):
    origin = objects[sym]
    door = objects.get(sym.upper(), origin)
    grid[origin] = grid[door] = '.'
    reach = get_reacheable_keys(origin, grid)
    if not reach:
        return 0
    res = []
    for (sym, pos, dist) in reach:
        r = dist + brute_force(objects, grid.copy(), sym)
        res.append(r)
    return min(res)


def brute_force_opt(objects, grid):
    current_min = 1000000
    def bf(objects, grid, trail="@", res=0):
        nonlocal current_min
        sym = trail[-1]
        if res >= current_min:
            return
        origin = objects[sym]
        door = objects.get(sym.upper(), origin)
        grid[origin] = grid[door] = '.'
        reach = get_reacheable_keys(origin, grid)
        if not reach:
            if res <= current_min:
                print(f"New candidate: {trail} ({res})")
                current_min = res
        for (sym, pos, dist) in sorted(reach, key=lambda r: r[2]):
            bf(objects, grid.copy(), trail + sym, res + dist)
    bf(objects, grid)
    return current_min


def solve_opt(s):
    objects, grid = parse_input(s)
    return brute_force_opt(objects, grid)

def solve(s):
    objects, grid = parse_input(s)
    return brute_force(objects, grid)

    
def get_reacheable_keys(origin, grid):
    """Return the set of key positions reacheable from `pos`"""
    visited = set()
    todo = deque([(0, origin)])
    reach = set()
    while todo:
        d, cur = todo.popleft()
        visited.add(cur)
        if grid[cur].islower():
            reach.add((grid[cur], cur, d))
        else:
            for x in get_neighbors(cur, grid):
                if x not in visited:
                    todo.append((d + 1, x))
    return reach


def distance(p1, p2, grid):
    """Distance between two connected points on the grid"""
    reach = get_reacheable_keys(p1, grid, stop_when=p2)
    for (sym, pos, dist) in reach:
        if pos == p2:
            return dist
    raise ValueError(f"{p1} and {p2} not connected")


def find_optimal_target(path):
    pass
    

from collections import deque
def find_closest_key(origin, grid):
    visited = set()
    todo = deque([(0, origin)])
    while todo:
        d, cur, prev = todo.popleft()
        if cur.islower():
            pass
        for x in get_neighbors(cur, grid):
            if x not in dists:
                heapq.heappush(todo, (d + 1, x, cur))
    return preds, dists


def path_to(target, preds):
    path = [target]
    while preds[target] is not None:
        target = preds[target]
        path.append(target)
    return list(reversed(path))

def find_shortest_paths(origin, grid):
    """Shorted path to every point in the territory"""
    dists = {}
    preds = {}
    todo = [(0, origin, None)]
    while todo:
        d, cur, prev = heapq.heappop(todo)
        dists[cur] = d
        preds[cur] = prev
        for x in get_neighbors(cur, grid):
            if x not in dists:
                heapq.heappush(todo, (d + 1, x, cur))
    return preds, dists
    
def target_paths():
    x, y, grid = parse_input()
    paths, dists = find_shortest_paths((x, y), grid)
    lin_paths = []
    for (x, y) in paths:
        c = grid[x, y]
        if (65 <= ord(c) <= 90) or (97 <= ord(c) <= 122):
            p = "".join(grid[px, py] for (px, py) in path_to((x, y), paths))
            lin_paths.append(p)
    return lin_paths

def uniquify(paths):
    unique = []
    for p in paths:
        for u in unique[:]:
            if p.startswith(u):
                unique.remove(u)
            if u.startswith(p):
                break
        else:
            unique.append(p)
    return unique

def trim(p):
    i = len(p) - 1
    while i >= 0 and (p[i].isupper() or p[i] == '.' or p[i] == "@"):
        i -= 1
    return p[:i + 1]
   
def required(paths):
    req = []
    for p in paths:
        t = trim(p)
        if t:
            req.append(t)
    return req
        
def display_unique_paths():
    print("\n".join(sorted(uniquify(required(uniquify(target_paths()))))))

def display_unique_deps():
    deps = [p.replace('.', '') + ' %s' % (len(p) - 1) for p in uniquify(required(uniquify(target_paths())))]
    print("\n".join(deps))
    
def level1():
    pass
    
if __name__ == "__main__":
    pass
    # solve_opt(read_input())
