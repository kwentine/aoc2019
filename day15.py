from day05 import run_async, parse_input
from random import choice
from copy import deepcopy
import sys
from time import sleep
from dijkstra import steps_to, path_to, find_shortest_paths

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4
COMMANDS = [NORTH, SOUTH, WEST, EAST]
DIRECTIONS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0)
}
STEP_TO_COMMAND = {v: k for (k, v) in DIRECTIONS.items()}
OPPOSITES = {
    NORTH:SOUTH,
    SOUTH:NORTH,
    EAST:WEST,
    WEST:EAST
}
CONTROLS = {
    "q": WEST,
    "s": SOUTH,
    "d": EAST,
    "z": NORTH 
}

OXYGEN_FOUND = 2
MOVE_SUCCESSFUL = 1
WALL_HIT = 0

prog =  parse_input(15)

def random_direction():
    return choice(COMMANDS)

def get_input():
    key = sys.stdin.read(1)
    try:
        return CONTROLS[key]
    except KeyError:
        return choice(COMMANDS)

def guess_input(prev_direction, success):
    if success:
        bias = (prev_direction,) * 4
        options = tuple(d for d in DIRECTIONS if d != OPPOSITES[prev_direction]) + bias
    else:
        if prev_direction in (NORTH, SOUTH):
            options = (EAST, WEST)
        else:
            options = (NORTH, SOUTH)
    return choice(options)
               
H = 50
W = 100

def display(droid, free_spots, walls, oxygen=None):
    FREE = "\033[1;34m.\033[m"
    WALL = "\033[47m \033[m"
    # DROID = "\033[1;32m\U0001F916\033[m"
    DROID = "\033[1;32mX\033[m" 
    OXYGEN = "\033[1;31m*\033[m"
    grid = [[WALL] * W for _ in range(H)]
    
    try:
        for (x, y) in free_spots:
            grid[y][x] = FREE
        for (x, y) in walls:
            grid[y][x] = WALL
        grid[25][50] = "X"
        grid[droid[1]][droid[0]] = DROID
        if oxygen is not None:
            grid[oxygen[1]][oxygen[0]] = OXYGEN
        print("\033[2J\033[1;1H")
        grid = "\n".join(''.join(row) for row in grid)
        print(grid)
    except IndexError:
        print(f"Invalid index: {x}, {y}")


def drive_robot(interactive=True):
    machine = run_async(prog)
    # Droid coordinates
    x, y = W // 2, H // 2
    free_spots = set()
    walls = set()
    oxygen = None
    next_move = None
    success = False
    try:
        # import pudb; pudb.set_trace()
        while True:
            display((x, y), free_spots, walls, oxygen)
            free_spots.add((x, y))
            report = machine.send(next_move)
            if report is None:
               if interactive:
                   next_move = get_input()
               else:
                   sleep(0.01)
                   next_move = guess_input(next_move, success)
            else:
                dx, dy = DIRECTIONS[next_move]
                next_pos = x + dx, y + dy
                success = report != WALL_HIT
                if report == MOVE_SUCCESSFUL:
                    x, y = next_pos
                elif report == OXYGEN_FOUND:
                    oxygen = x, y = next_pos
                elif report == WALL_HIT:
                    walls.add(next_pos)
                else:
                    raise RuntimeError("Unknown report code:", report)
        raise StopIteration("Oxygen: {oxygen}")
    except StopIteration:
        print('Oxygen not found')
    

def goto_pos(steps):
    """Returns machine accepting next step inputs"""
    machine = run_async(prog)
    for s in steps:
        machine.send(None)
        machine.send(STEP_TO_COMMAND[s])
    return machine

oxygen = None

def get_neighbors(target, preds):
    global oxygen
    steps = steps_to(target, preds)
    machine = goto_pos(steps)
    neighbors = []
    x, y = target
    for d in COMMANDS:
        dx, dy = DIRECTIONS[d]
        machine.send(None)
        report = machine.send(d)
        if report == WALL_HIT:
            continue
        n = x + dx, y + dy
        if report == OXYGEN_FOUND:
            print('Oxygen found at', n)
            oxygen = n
        neighbors.append(n)
        machine.send(None)
        machine.send(OPPOSITES[d])
    return neighbors

def explore():
    preds, _ = find_shortest_paths((50, 25), get_neighbors)
    display((50, 25), preds, [])


def level2():
    # cached_preds, _ = find_shortest_paths((0,0), get_neighbors)
    from maze import cached_preds
    oxygen = (16, 12) 
    # print('Exploration complete')
    # print(cached_preds)
    
    def get_neighbors_cached(cur, preds):
        children = [k for (k, v) in cached_preds.items() if v == cur]
        if cached_preds.get(cur):
            children.append(cached_preds.get(cur))
        return children
    
    _, dist = find_shortest_paths(oxygen, get_neighbors_cached)
    print(max(dist.values()))
        
        

level2()
            
# if __name__ == "__main__":
#     import tty, termios
#     restore = termios.tcgetattr(sys.stdin)
#     tty.setcbreak(sys.stdin.fileno())
#     try:
#         drive_robot(interactive=False)
#     except StopIteration as e:
#         print(e)
#     finally:
#         termios.tcsetattr(sys.stdin, termios.TCSADRAIN, restore)

