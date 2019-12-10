from fractions import Fraction

asteroids = []
with open('data/day10.txt') as f:
    for (y, l) in enumerate(f):
        for (x, c) in enumerate(l.strip()):
            if c == '#':
                asteroids.append((x, y))

slope_cache = {}                
def slope(a0, a):
    x0, y0 = a0
    x, y = a
    if x == x0:
        return (None, y > y0)
    return (Fraction(y - y0, x - x0), x > x0)

visible = {
    a0: set(slope(a0, a) for a in asteroids if a != a0)
    for a0 in asteroids
}

print(max((len(v), a) for (a, v) in visible.items()))    



