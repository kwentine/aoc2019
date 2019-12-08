from collections import Counter
from itertools import product

with open('data/day08.txt') as f:
    code = [int(i) for i in f.read().strip()]

HEIGHT = 6
WIDTH = 25

def decode(code, h=HEIGHT, w=WIDTH):
    img = [[""] * w for _ in range(h)]
    layers = layer_list(code, h, w)
    for (i, j) in product(range(h), range(w)):
        for l in layers:
            c = l[i * w + j] 
            if  c < 2:
                img[i][j] = "\u25AE" if c else " "
                break
    return img


def layer_list(code, h=HEIGHT, w=WIDTH):
    size = h * w
    return [code[i:i + size] for i in range(0, len(code), size)]


def level1():
    size = WIDTH * HEIGHT
    z, o, t = [size] * 3
    for l in layer_list(code):
        c = Counter(l)
        if c[0] <= z:
            z, o, t = c[0], c[1], c[2]
    return o * t


def level2():
    img = decode(code)
    return "\n".join("".join(l) for l in img)
    
if __name__ == "__main__":
    print("Level 1:", level1())
    print("Level 2:")
    print(level2())
    
