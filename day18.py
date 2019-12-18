import heapq
from collections import defaultdict

def read_input():
    with open('data/day18.txt') as f:
        return f.read()

def parse_input():
    grid = defaultdict(str)
    x, y = 0, 0
    x0, y0 = 0, 0
    for c in read_input():
        if c == '\n':
            y += 1
            x = 0
            continue
        if c == '@':
            x0, y0  = x, y
        grid[(x, y)] = c
        x += 1
    return x0, y0, grid

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
    
def get_neighbors(cur, grid):
    x, y = cur
    for (dx, dy) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if grid[nx, ny] and grid[nx, ny] != '#':
            yield (nx, ny)
    
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

def path_to(target, preds):
    path = [target]
    while preds[target] is not None:
        target = preds[target]
        path.append(target)
    return list(reversed(path))
