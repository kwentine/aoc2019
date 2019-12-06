from itertools import chain

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def parse_input():
    with open('data/day03.txt') as f:
        return f.readlines()

def segment(start, course, length):
    """Half-open segment ] start, start + direction * length ]"""
    x0, y0, d0 = start
    vx, vy = DIRECTIONS[course]
    return tuple((x0 + (k + 1) * vx, y0 + (k + 1) * vy, d0 + k + 1) for k in range(length))

def path(spec):
    start = (0, 0, 0)
    for s in spec:
        course, length = s[0], int(s[1:])
        seg = segment(start, course, length)
        yield from seg
        start = seg[-1]

def trail(p):
    return set((x, y) for (x, y, d) in p)

def weighted_trail(p):
    return {(x, y): d for (x, y, d) in reversed(list(p))} 
        
def nearest_crossing(w1, w2):
    w1, w2 = w1.split(','), w2.split(',')
    return min(abs(x) + abs(y) for (x, y) in trail(path(w1)) & trail(path(w2)))

def fastest_crossing(w1, w2):
    w1, w2 = w1.split(','), w2.split(',')
    wt1, wt2 = weighted_trail(path(w1)), weighted_trail(path(w2))
    return min(wt1[(x, y)] + wt2[(x, y)] for (x, y) in set(wt1) & set(wt2))

# TODO: Print two colored path in the terminal
def plot(p1, p2):
    origin = (0, 0)
    xrng = set(pt[0] for pt in chain(p1, p2, (origin,)))
    yrng = set(pt[1] for pt in chain(p1, p2, (origin,)))
    xmin, xmax = min(xrng), max(xrng)
    ymin, ymax = min(yrng), max(yrng)
    w = xmax - xmin
    h = ymax - ymin    
    grid = [[b'.'] * w for _ in range(h)]
    draw(p1, grid)
    draw(p2, grid)
    
def level1():
    w1, w2 = parse_input()
    return nearest_crossing(w1, w2)

def level2():
    w1, w2 = parse_input()
    return fastest_crossing(w1, w2)

if __name__ == "__main__":
    print(level2())
