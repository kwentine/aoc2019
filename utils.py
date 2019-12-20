import sys
from typing import Any, Callable, Union, List, IO, Tuple, Dict

FILE_NAME_FMT = 'data/day%02d.txt' 

CmapCondT = Union[Callable[[str], bool], str]
CmapT = List[Tuple[CmapCondT, str]]
CoordT = Tuple[int, int]

def read_input(day: int, *, strip: bool = True) -> str:
    filename = FILE_NAME_FMT % day
    with open(filename) as f:
        s = f.read()
    if strip:
        s = s.strip()
    return s

def get_input(day: int, parser=lambda x: x,* ,strip: bool = True) -> Any:
    return parser(read_input(day, strip=strip))


def _apply_cmap(c: str, cmap: CmapT) -> str:
    for (pred, fmt) in cmap:
        if callable(pred):
            p = pred(c)
        else:
            p = c == pred
        if p:
            return fmt.format(c)
    return c

def render(grid: Dict[CoordT, str], cmap: CmapT, color: bool = True) -> str:
    xmax = max(x for (x, y) in grid)
    ymax = max(y for (x, y) in grid)
    buff = []
    for y in range(ymax + 1):
        for x in range(xmax + 1):
            c = grid[x, y]
            buff.append(_apply_cmap(c, cmap))
        buff.append("\n")
    return "".join(buff)

def display(grid: Dict[CoordT, str], cmap: CmapT, stdout: IO = None) -> None:
    if stdout is None:
        stdout = sys.stdout
    try:
        color = stdout.isatty()
    except AttributeError:
        color = False
    stdout.write(render(grid, cmap, color))
