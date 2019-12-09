from day05 import run_async


def run_until_complete(machine, inputs=None):
    if inputs is None:
        inputs = []
    inputs = inputs[::-1]
    outputs = []
    out = None
    try:
        while True:
            out = machine.send(out)
            if out is None:
                out = inputs.pop()
            else:
                outputs.append(out)
    except StopIteration:
        return outputs


with open('data/day09.txt') as f:
    prog = [int(i) for i in f.read().strip().split(',')]

machine = run_async(prog)

print(run_until_complete(machine, inputs=[2]))

    
     
    
