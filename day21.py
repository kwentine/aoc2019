from day05 import run_async, parse
from utils import get_input, animate_frames
from typing import Union, List, Generator


prog = get_input(21, parse)

def read_output(machine: Generator, buff: List[int] = None):
    if buff is None:
        buff = []
    out = next(machine)
    while out is not None:
        buff.append(out)
        try:
            out = next(machine)
        except StopIteration:
            out = None
    return buff

def ascii_to_str(buff: List[int]):
    out = []
    for c in buff:
        if not 0 <= c <= 127:
            raise ValueError(f"Outside ASCII range: {c}")
        out.append(chr(c))
    return "".join(out)
        
def feed_input(machine: Generator, buff: List[int]):
    out = None
    idx = 0
    while out is None:
        out = machine.send(buff[idx])
        idx += 1
    assert idx == len(buff), "Input interrupted after {idx} sent."
    return out

def run_interactive(instr, speed=1):
    machine = run_async(prog)
    print(ascii_to_str(read_output(machine)))
    print(instr)
    out = feed_input(machine, [ord(c) for c in instr])
    buff = read_output(machine, [out])
    s = ascii_to_str(buff)
    frames = s.split("\n\n")
    animate_frames(frames, speed)

sol1 = """\
OR A J
NOT A T
OR J T
AND A T
AND B T
AND C T
NOT T J
AND D J
WALK
"""
"""NOT (A OR B OR C) AND D

Jump if we cant't make three steps ahead and will land safely. 
"""

sol2 = """\
OR A J
NOT A T
OR J T
AND A T
AND B T
AND C T
NOT T J
OR T T
AND J T
AND D J
OR E T
OR H T
AND T J
RUN
"""
"""NOT (A OR B OR C) AND D AND (E OR H)

Same condition as solution 1, but ensure we can jump immediatly again
if needed.
"""
    
        
    
    
