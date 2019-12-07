from itertools import permutations
from day05 import run


with open('data/day07.txt') as f:
    prog = [int(i) for i in f.readline().strip().split(',')]

phases = permutations(range(5), 5)
max_output = 0
max_config = None
for config in phases:
    inpt = 0
    for p in config:
        inpt = run(prog, (p, inpt))
    if inpt >= max_output:
        max_output, max_phase = inpt, config

print(f"Max thruster signal {max_output} "
      f"for configuration {','.join(str(i) for i in max_phase)}")
