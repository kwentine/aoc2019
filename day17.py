from day05 import run_async


def get_prog():
    with open("data/day17.txt") as f:
        return [int(i) for i in f.read().strip().split(',')]

def get_input_string():
    with open("data/day17.txt") as f:
        prog = [int(i) for i in f.read().strip().split(',')]
    return "".join([chr(i) for i in run_async(prog)])

def parse_input():
    return parse_grid(s)


DIRECTIONS = {
    '>': (1, 0),
    '<': (-1, 0),
    '^': (0, -1),
    'v': (0, 1)
}


MAIN = [ord(c) for c in 'A,A,B,C,B,A,C,B,C,A']
ROUTINES = {
    ord('A'): [ord(c) for c in "L,6,R,12,L,6,L,8,L,8"],
    ord('B'): [ord(c) for c in "L,6,R,12,R,8,L,8"],
    ord('C'): [ord(c) for c in "L,4,L,4,L,6"],
}


def parse_grid(s):
    grid, row = [], []
    x, y, dx, dy, h, w, found = 0, 0, 0, 0, 0, 0, 0
    for (idx, c) in enumerate(s):
        if c == '\n':
            # Trailing duplicate newlines
            if not row:
                continue
            grid.append(row)
            row = []
            h += 1            
            if not w:
                w = idx
            continue
        row.append(c)
        if not found and c in ('<>^v'):
            found = True
            x = idx % (w + 1)
            y = h
            dx, dy = DIRECTIONS[c]
    return x, y, dx, dy, h, w, grid
        

def serialize_grid(grid):
    return "\n".join(''.join(r) for r in grid)

def level1():
    h, w, grid = parse_input()
    dirs = ((0,0), (1, 0), (-1, 0), (0, 1), (0, -1))
    res = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            for (dx, dy) in dirs:
                if grid[y + dy][x + dx] != '#':
                    break
            else:
                grid[y][x] = "O"
                res += x * y
    print(serialize_grid(grid))
    print(res)


def forward(x, y, dx, dy, grid):
    """Return the maximum of steps that can be made"""
    res = 0
    nx, ny = x + dx, y + dy
    try:
        while nx >= 0 and ny >= 0 and grid[ny][nx] == '#':
            res += 1
            nx, ny = nx + dx, ny + dy
    except IndexError:
        pass
    return res
    
def left(dx, dy):
    return dy, -dx

def right(dx, dy):
    return -dy, dx

def generate_instructions(x, y, dx, dy, grid):
    inst = []
    while True:
        dx, dy = left(dx, dy)
        n = forward(x, y, dx, dy, grid)
        if n:
            print(f'LEFT {n}')
            inst.append('L')
            inst.append(str(n))
        else:
            dx, dy = -dx, -dy
            n = forward(x, y, dx, dy, grid)
            if not n:
                print('ABORT')
                return inst
            print(f'RIGHT {n}')
            inst.append('R')
            inst.append(str(n))
        x, y = x + n * dx, y + n * dy

        
from time import sleep
def level2():
    prog = get_prog()
    prog[0] = 2
    machine = run_async(prog)

    # Print initial map
    outputs = []
    out = machine.send(None)
    while out:
        outputs.append(chr(out))
        out = next(machine)
    print("".join(outputs))

    for c in MAIN:
        machine.send(c)
    outputs = []
    out =  machine.send(ord('\n'))
    while out:
        outputs.append(chr(out))
        out = next(machine)
    print("".join(outputs))
    for instr in ROUTINES[ord('A')]:
        machine.send(instr)
    outputs = []
    out =  machine.send(ord('\n'))
    while out:
        outputs.append(chr(out))
        out = next(machine)
    print("".join(outputs))
    for instr in ROUTINES[ord('B')]:
        machine.send(instr)
    outputs = []
    out =  machine.send(ord('\n'))
    while out:
        outputs.append(chr(out))
        out = next(machine)
    print("".join(outputs))
    for instr in ROUTINES[ord('C')]:
        machine.send(instr)
    outputs = []
    out =  machine.send(ord('\n'))
    while out:
        outputs.append(chr(out))
        out = next(machine)
    print("".join(outputs))
    machine.send(ord('y'))
    outputs = []
    out = machine.send(ord('\n'))
    while out and out < 255:
        outputs.append(chr(out))
        out = next(machine)
    
    frames = "".join(outputs).split('\n\n')
    for f in frames:
        print("\033[2J\033[1;1H")
        print(f)
        sleep(0.1)
    
    print(out)

level2()
            

    
