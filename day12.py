"""Day 12"""

from itertools import combinations

moons = [
    ([-9, -1, -1], [0] * 3),
    ([2, 9, 5], [0] * 3),
    ([10, 18, -12], [0] * 3),
    ([-6, 15, -7], [0] * 3)
]


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

moon_pairs = combinations(moons, 2)
for step in range(1000):
    for (m1, m2) in moon_pairs:
        apply_gravity(m1, m2)
    for m in moons:
        apply_velocity(m)

print(sum(energy(m) for m in moons))
