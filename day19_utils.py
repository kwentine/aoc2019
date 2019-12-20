from day05 import run_async

def read_input():
    with open("data/day19.txt") as f:
        return f.read().strip()
        
prog = [int(x) for x in read_input().split(',')]
    
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

def display(x, y, h, w):
    print(x)
    print(''.join([' ' if i % 10 else 'v' for i in range(w)]))
    for j in range(h):
        for i in range(w):
            fmt = BG_YELLOW if is_pulled(x + i, y + j) else BG_GREY
            print(fmt % ".", end="")
        print(format(j + y , "03d"))
    print(''.join(['.' if i % 10 else '^' for i in range(w)]))

# y = 100 / 61 x    
# y = 184 / 100 * x
# y = 100 / 49 * x
