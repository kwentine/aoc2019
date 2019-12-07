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
OP_HALT = "99"
LOAD = "0"
LOAD_CONST = "1"


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


def run_async(prog):
    ip = 0
    mem = prog[:]
    while True:
        op, modes = parse_instruction(mem[ip])
        if op in (OP_ADD, OP_MUL, OP_EQ, OP_LT):
            p1, p2 = get_args(ip + 1, modes[:2], mem)
            mem[mem[ip + 3]] = OP_FUNCS[op](p1, p2)
            ip += 4
        elif op == OP_IN:
            inpt = yield
            mem[mem[ip + 1]] = inpt 
            ip += 2
        elif op == OP_OUT:
            output = load(modes[0], ip + 1, mem) 
            yield output
            ip += 2
        elif op in (OP_JT, OP_JF):
            flag, addr = get_args(ip + 1, modes[:2], mem)
            ip = OP_FUNCS[op](ip, flag, addr)
        elif op == OP_HALT:
            return
        else:
            raise RuntimeError(f"Unknown instruction at address {ip}: {mem[ip]}")


def load(mode: str, addr: int, mem: List[int]) -> int:
    ptr_or_val = mem[addr]
    return ptr_or_val if mode == LOAD_CONST else mem[ptr_or_val]


def get_args(ip: int, modes: Sequence[str], mem: List[int]) -> Tuple[int, ...]:
    return tuple(load(m, ip + i, mem) for (i, m) in enumerate(modes))


def parse_instruction(i: int) -> Tuple[str, Tuple[str, ...]]:
    s = f"{i:05d}"
    op = s[3:]
    modes = tuple(s[2::-1])
    return op, modes


def parse_input() -> List[int]:
    with open("data/day05.txt") as f:
        return [int(i) for i in f.read().strip().split(",")]


def level1() -> None:
    prog = parse_input()
    run(prog)


if __name__ == "__main__":
    level1()
