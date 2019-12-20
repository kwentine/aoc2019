from utils import get_input
from itertools import product
from collections import defaultdict
from day05 import run_async

DAY = 11

def parse(s):
    return [int(x) for x in s.split(',')]
        
prog = get_input(19, parse)
    
def is_pulled(x, y):
    machine = run_async(prog)
    next(machine)
    machine.send(x)
    return machine.send(y)

def hsection(y, x=0):
    while not is_pulled(x, y):
        x += 1
    x0 = x
    while is_pulled(x + 1, y):
        x += 1
    return (x0, x)

BG_YELLOW = "\033[37;43m%s\033[m"
BG_GREY = "\033[37;40m%s\033[m"

def glyph(x, y):
    p = is_pulled(x, y)
    fmt = BG_YELLOW if p else BG_GREY
    return fmt % '.'

def draw(x, y, h, w=None):
    w = w or h
    print(x)
    print(''.join([' ' if i % 10 else 'v' for i in range(w)]))
    for j in range(h):
        for i in range(w):
            print(glyph(x + i, y + j), end="")
        print(format(j + y , "03d"))
    print(''.join(['.' if i % 10 else '^' for i in range(w)]))

# y = 100 / 61 x    
# y = 184 / 100 * x
# y = 100 / 49 * x
def get_slopes(y):
    xmin, xmax = hsection(y)
    return (y/xmax, y/xmin)

S_MIN, S_MAX = get_slopes(100)
SIZE = 100

def safe_offset(y):
    fxmin = y / S_MAX
    return max(int(fxmin) - 10, 0)

def square_fits(y):
    """Check if square fits at altitude `y`"""
    offset = safe_offset(y)
    assert not is_pulled(offset, y)
    _, xmax = hsection(y, offset)
    ymax = y + SIZE - 1
    offset = safe_offset(ymax)
    assert not is_pulled(offset, ymax)
    xmin, _ = hsection(ymax)
    return xmax >= xmin + SIZE - 1


X_OPT =   SIZE * (1 + S_MIN) / (S_MAX - S_MIN)
Y_OPT = S_MAX * X_OPT - SIZE


def level1():
    return sum(is_pulled(x, y) for (x, y) in product(range(50), range(50)))


def level2():
    assert is_pulled(X_OPT, Y_OPT)
    y = int(Y_OPT) + 1
    while True:
        for i in range(10, 0, -1):
            if square_fits(y - i):
                y -= i
                print(f"Fits at {y}")
                break
        else:
            print(f"Does not fit below {y}")
            break
    xmin, xmax = hsection(y)
    print(f"Upper right: ({xmax}, {y})")
    print(f"Closest: ({xmax - SIZE + 1}, {y})")
    ans = 10000 * (xmax - SIZE + 1) + y
    print(f"{ans}")


if __name__ == "__main__":
    # level2() # 624, 1175
    draw(619, 1165, 100, 100)
    # draw(623, 1177, 100, 100)
    # draw(620, 1177, 100, 100)
    pass
