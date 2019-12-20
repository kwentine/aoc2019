from typing import Any

FILE_NAME_FMT = 'data/day%02d.txt' 

def read_input(day: int) -> str:
    filename = FILE_NAME_FMT % day
    with open(filename) as f:
        return f.read().strip()

def get_input(day: int, parser=lambda x: x) -> Any:
    return parser(read_input(day))
