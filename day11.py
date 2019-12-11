from day05 import run_async
from collections import defaultdict

def drive_robot(machine, initial=0, return_frames=False):
    # Panel grid
    grid = defaultdict(int)
    visited = set()
    # Robot position
    x, y = 0, 0
    dx, dy = 0, -1
    grid[(0, 0)] = initial
    frames = []
    try:
        while True:
            frames.append((grid.copy(), (x, y), (dx, dy)))
            visited.add((x, y))
            machine.send(None)
            grid[(x, y)] = machine.send(grid[(x, y)])
            turn = machine.send(None)
            if not turn:
                dx, dy = dy, -dx
            else:
                dx, dy = -dy, dx
            x, y = x + dx, y + dy
    except StopIteration:
        return frames if return_frames else frames[-1]


def parse_input():
    with open('data/day11.txt') as f:
        prog = [int(i) for i in f.read().strip().split(',')]
    return prog


ROBOTS = {
    (1, 0): '>',
    (0, 1): 'v',
    (-1, 0): '<',
    (0, -1): '^'
}

def draw(grid, xmin=None, xmax=None, ymin=None, ymax=None, robot=None, direction=None):
    xmin = xmin or min(x for (x, y) in grid)
    xmax = xmax or max(x for (x, y) in grid)
    ymin = ymin or min(y for (x, y) in grid)
    ymax = ymax or max(y for (x, y) in grid)
    w = xmax - xmin + 1
    h = ymax - ymin + 1
    img = [[' '] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if grid[(x + xmin, y + ymin)]:
                img[y][x] = "#"
    if robot and direction:
        xr, yr = robot
        img[yr - ymin][xr - xmin] = f"\033[34;1m{ROBOTS[direction]}\033[0m"
    return "\n".join("".join(row) for row in img)



def step1():
    prog = parse_input()
    grid = drive_robot(run_async(prog))
    return len(grid)

def step2():
    prog = parse_input()
    grid = drive_robot(run_async(prog), initial=1)
    return draw(grid)

from time import sleep

def animate():
    prog = parse_input()
    frames = drive_robot(run_async(prog), initial=1, return_frames=True)
    (final, _, _) = frames[-1]
    xmin = min(x for (x, y) in final)
    xmax = max(x for (x, y) in final)
    ymin = min(y for (x, y) in final)
    ymax = max(y for (x, y) in final)
    #import pdb; pdb.set_trace()
    for (grid, robot, direction) in frames:
        # Clear screen and move cursor to top-left
        print("\033[2J\033[1;1H")
        print(draw(grid, xmin, xmax, ymin, ymax, robot, direction))
        sleep(0.1)
        

if __name__ == "__main__":
    animate()
    
