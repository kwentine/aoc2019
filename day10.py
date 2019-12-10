from collections import defaultdict
import math

def parse_input():
    asteroids = []
    with open('data/day10.txt') as f:
        for (y, l) in enumerate(f):
            for (x, c) in enumerate(l.strip()):
                if c == '#':
                    asteroids.append((x, y))
    return asteroids

def step1():
    asteroids = parse_input()
    visible = {
        a0: set(angle(a[0] - a0[0], a[1] - a0[1]) for a in asteroids if a != a0)
        for a0 in asteroids
    }
    return max((len(v), a) for (a, v) in visible.items())

def step2():
    asteroids = parse_input()
    by_angle = defaultdict(list)
    for center in asteroids:
        cx, cy = center
        for target in asteroids:
            if target == center:
                continue
            tx, ty = target
            theta = angle(tx - cx, ty - cy)
            d = dist(tx - cx, ty - cy) 
            by_angle[theta].append((d, tx, ty))
    x, y = list(targets(by_angle))[199]
    return 100 * x + y

def dist(x, y):
    return x * x + y * y 
    
def slope(x, y):
    t = angle(x, y)
    return t if x > 0 else t - math.pi

def angle(x, y):
    if x == 0:
        return math.copysign(1, y) * math.pi / 2
    if x > 0:
        return math.atan(y/x)
    if x < 0:
        x, y = -x, -y
        return math.atan(y/x) + math.pi

from itertools import cycle
def targets(by_angle):
    by_angle = {k: sorted(v, reverse=True) for (k, v) in by_angle.items()}
    n = len(by_angle)
    for k in cycle(sorted(by_angle)):
        if n == 0:
            break
        try:
            d, x, y = by_angle[k].pop()
        except IndexError:
            n -= 1
        else:
            yield (x, y)
            
    
if __name__ == "__main__":
    # print(step1())
    print(step2())


