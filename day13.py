"""Day 13"""
from day05 import run_async, parse_input
from time import sleep
import select
import sys
import termios

def level1():
    prog = parse_input(day=13)
    machine = run_async(prog)
    outputs = list(machine)
    blocks = set()
    for i in range(0, len(outputs), 3):
        x, y, t = outputs[i:i+3]
        if t == 2:
            blocks.add((x,y))
        elif t == 4:
            try:
                blocks.remove((x,y))
            except KeyError:
                pass
    print(len(blocks))

JOYSTICK_KEYS = {
    'a': -1,
    'z': 0,
    'e': 1
}

GLYPHS = {
    0: ' ',
    1: '#',
    2: '*',
    3: '_',
    4: '@'
}

def get_input():
    move = 0
    rlist, _, _ = select.select([sys.stdin], [], [], 0.2)
    if rlist:
        c = sys.stdin.read(1)
        move = JOYSTICK_KEYS.get(c, 0)
    return move

import tty
def level2():
    grid = [[' '] * 40 for _ in range(25)]
    prog = parse_input(day=13)
    prog[0] = 2
    machine = run_async(prog)
    out = None
    score = 0
    try:
        restore = termios.tcgetattr(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        while True:
            out = machine.send(out)
            # We get some output
            if out is not None:
                x = out
                y = next(machine)
                t = next(machine)
                if x < 0:
                    score = t
                else:
                    grid[y][x] = GLYPHS.get(t, '?')
            else:
                print("\033[2J\033[1;1H")
                print(f"Score: {score}")
                print("\n".join(''.join(r) for r in grid))
                out = get_input()
                sleep(0.2)
    except StopIteration:
        print("\033[33mGAME OVER\033[m")
    finally:
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, restore)

level2()
            
        
    
