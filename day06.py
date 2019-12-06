"""Day 6: Universal Orbit Map"""


def lazy_orbit_depths(orbits):
    orbit_depths = {"COM": lambda: 0}
    for (center, satellite) in orbits:

        def count_orbits(center=center):
            return orbit_depths[center]() + 1

        orbit_depths[satellite] = count_orbits
    return orbit_depths


def build_orbit_tree(orbits):
    tree = {k: v for (v, k) in orbits}
    tree["COM"] = None
    return tree


def path_to_com(satellite, tree):
    parent = tree[satellite]
    path = []
    while parent is not None:
        path.append(parent)
        parent = tree[parent]
    return tuple(reversed(path))


def distance(sat1, sat2, tree):
    p1, p2 = path_to_com(sat1, tree), path_to_com(sat2, tree)
    prefix_length = len([i for (i, j) in zip(p1, p2) if i == j])
    return len(p1) + len(p2) - 2 * prefix_length


def parse_input():
    with open("data/day06.txt") as f:
        return [l.split(")") for l in f.read().split("\n") if l.strip()]


def level1():
    orbits = parse_input()
    lazy_depths = lazy_orbit_depths(orbits)
    return sum(f() for f in lazy_depths.values())


def level2():
    orbits = parse_input()
    tree = build_orbit_tree(orbits)
    return distance("YOU", "SAN", tree)


if __name__ == "__main__":
    print(f'Level 1: {level1()}')
    print(f"Level 2: {level2()}")
