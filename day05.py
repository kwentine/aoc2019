"""Day 5: Sunny with a Chance of Asteroids"""
from typing import Sequence, Tuple, List, Callable, Dict, Optional
from operator import add, mul, eq, lt

OP_ADD = "01"
OP_MUL = "02"
OP_IN = "03"
OP_OUT = "04"
OP_JT = "05"
OP_JF = "06"
OP_LT = "07"
OP_EQ = "08"
OP_REBASE = "09"
OP_HALT = "99"
LOAD = "0"
LOAD_CONST = "1"
LOAD_REL = "2"

OP_FUNCS = {
    OP_ADD: add,
    OP_MUL: mul,
    OP_EQ: eq,
    OP_LT: lt,
    OP_JT: lambda ip, flag, addr: addr if flag else ip + 3,
    OP_JF: lambda ip, flag, addr: addr if not flag else ip + 3,
}  # type: Dict[str, Callable[..., int]]


def run(prog: List[int], inputs: Optional[Tuple[int, ...]] = None) -> None:
    ip = 0
    mem = prog[:]
    if inputs is None:
        inputs = ()
    next_input = 0
    output = None
    while True:
        op, modes = parse_instruction(mem[ip])
        if op in (OP_ADD, OP_MUL, OP_EQ, OP_LT):
            p1, p2 = get_args(ip + 1, modes[:2], mem)
            mem[mem[ip + 3]] = OP_FUNCS[op](p1, p2)
            ip += 4
        elif op == OP_IN:
            addr = mem[ip + 1]
            try:
                inpt = inputs[next_input]
                next_input += 1
            except IndexError:
                inpt = int(input("Input  : "))
            mem[addr] = inpt 
            ip += 2
        elif op == OP_OUT:
            output = load(modes[0], ip + 1, mem)
            # print("Output :", output)
            ip += 2
        elif op in (OP_JT, OP_JF):
            flag, addr = get_args(ip + 1, modes[:2], mem)
            ip = OP_FUNCS[op](ip, flag, addr)
        elif op == OP_HALT:
            break
        else:
            raise RuntimeError(f"Unknown instruction at address {ip}: {mem[ip]}")
    return output

# TODO: Cleanup, refactor
# - Get modes without casting to string
# - Write a test suite with all provided examples
EXTRA_MALLOC_FACTOR = 10
def run_async(prog, extra_malloc=EXTRA_MALLOC_FACTOR):
    ip = 0
    rel_base = 0
    mem = prog[:]
    mem += [0] * (len(prog) * extra_malloc)
    while True:
        op, modes = parse_instruction(mem[ip])
        if op in (OP_ADD, OP_MUL, OP_EQ, OP_LT):
            p1, p2 = get_args(ip + 1, modes[:2], rel_base, mem)
            w_addr = mem[ip + 3]
            if modes[2] == LOAD_REL:
                w_addr += rel_base
            mem[w_addr] = OP_FUNCS[op](p1, p2)
            ip += 4
        elif op == OP_IN:
            inpt = yield
            w_addr = mem[ip + 1]
            if modes[0] == LOAD_REL:
                w_addr += rel_base
            mem[w_addr] = inpt 
            ip += 2
        elif op == OP_OUT:
            output = load(modes[0], ip + 1, rel_base, mem) 
            yield output
            ip += 2
        elif op in (OP_JT, OP_JF):
            flag, addr = get_args(ip + 1, modes[:2], rel_base, mem)
            ip = OP_FUNCS[op](ip, flag, addr)
        elif op == OP_REBASE:
            delta = load(modes[0], ip + 1, rel_base, mem)
            rel_base += delta
            ip += 2
        elif op == OP_HALT:
            return
        else:
            raise RuntimeError(f"Unknown instruction at address {ip}: {mem[ip]}")


def load(mode, addr, rel_base, mem):
    param = mem[addr]
    # Absolute addressing
    if mode == LOAD:
        return mem[param]
    if mode == LOAD_REL:
        return mem[param + rel_base]
    if mode == LOAD_CONST:
        return param
    raise RuntimeError("Invalid addressing mode for instruction @{addr}: {mode}")

def get_args(ip, modes, rel_base, mem):
    return tuple(load(m, ip + i, rel_base, mem) for (i, m) in enumerate(modes))


def parse_instruction(i: int) -> Tuple[str, Tuple[str, ...]]:
    s = f"{i:05d}"
    op = s[3:]
    modes = tuple(s[2::-1])
    return op, modes


def parse_input(day=5) -> List[int]:
    with open(f"data/day{day:02d}.txt") as f:
        return [int(i) for i in f.read().strip().split(",")]


def level1() -> None:
    prog = parse_input()
    run(prog)


if __name__ == "__main__":
    level1()
