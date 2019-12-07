from itertools import permutations, cycle
from day05 import run, run_async

with open('data/day07.txt') as f:
        prog = [int(i) for i in f.readline().strip().split(',')]

def level1():
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


def level2():
    phases = permutations(range(5, 10), 5)
    max_output = 0
    max_config = None
    for config in phases:
        amps = [run_async(prog) for l in "ABCDE"]
        initial = list(reversed(config))
        inpt = output = 0
        try:
            for amp in cycle(amps):
                amp.send(None)
                if initial:
                    amp.send(initial.pop())
                inpt = amp.send(inpt)
        except StopIteration:
            output = inpt
        if output >= max_output:
            max_output, max_config = output, config
    print(f"Max thruster signal {max_output} "
          f"for configuration {','.join(str(i) for i in max_config)}")
 
        
if __name__ == "__main__":
    level2()
