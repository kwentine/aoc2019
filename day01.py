def required_fuel(mass):
    return max(mass // 3 - 2, 0)

def part1():
    total = 0
    for line in open('data/day01.txt'):
        mass = int(line)
        fuel = required_fuel(mass)
        total += fuel
    return total

def part2():
    with open('data/day01.txt') as f:
        return sum(total_required_fuel(int(n)) for n in f)
    
def total_required_fuel(mass, total=0):
    if mass <= 0:
        return total
    mass = required_fuel(mass)
    return total_required_fuel(mass, total + mass)


if __name__ == "__main__":
    import sys
    level_solvers = (part1, part2)
    try:
        level = int(sys.argv[1])
    except IndexError:
        level = 1
    result = level_solvers[level - 1]()
    print(result)
