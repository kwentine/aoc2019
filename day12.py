"""Day 12"""

from itertools import combinations


def apply_gravity(m1, m2):
    for i in range(3):
        dv1, dv2 = apply_gravity1d(m1[0][i], m2[0][i])
        m1[1][i] += dv1
        m2[1][i] += dv2

def apply_gravity1d(x, y):
    if x == y: return (0, 0)
    if x < y: return (1, -1)
    if x > y: return (-1, 1)

def apply_velocity(m):
    pos, vel = m
    for i in range(3):
        pos[i] += vel[i]

def energy(m):
    pos, v = m
    return sum(abs(x) for x in pos) * sum(abs(x) for x in v)


def step(moons, n=0):
    moon_pairs = list(combinations(moons, 2))
    for _ in range(n):
        for (m1, m2) in moon_pairs:
            apply_gravity(m1, m2)
        for m in moons:
            apply_velocity(m)
    return moons

def project(moons, dim):
    return tuple((m[0][dim], m[1][dim]) for m in moons)

def step_until(moons):
    initial_x = project(moons, 0)
    initial_y = project(moons, 1)
    initial_z = project(moons, 2)
    orbits = {}
    moon_pairs = list(combinations(moons, 2))
    n_steps = 0
    while len(orbits) < 3:
        for (m1, m2) in moon_pairs:
            apply_gravity(m1, m2)
        for m in moons:
            apply_velocity(m)
        n_steps += 1
        if initial_x == project(moons, 0):
            print(f'x orbit for n={n_steps}')
            orbits.setdefault('x', n_steps)
        if initial_y == project(moons, 1):
            print(f'y orbit for n={n_steps}')
            orbits.setdefault('y', n_steps)
        if initial_z == project(moons, 2):
            print(f'z orbit for n={n_steps}')
            orbits.setdefault('z', n_steps)
    return orbits
        
    

moons = [
    ([-9, -1, -1], [0] * 3),
    ([2, 9, 5], [0] * 3),
    ([10, 18, -12], [0] * 3),
    ([-6, 15, -7], [0] * 3)
]

def level1():
    moons = [
    ([-9, -1, -1], [0] * 3),
    ([2, 9, 5], [0] * 3),
    ([10, 18, -12], [0] * 3),
    ([-6, 15, -7], [0] * 3)
    ]
    step(moons, 1000)
    print(sum(energy(m) for m in moons))

def level2():
    orbits = step_until(moons)
    print(orbits)

level2()
