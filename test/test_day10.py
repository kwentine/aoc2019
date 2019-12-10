import sys

print("\n".join(sys.path))

import pytest
import math
from day10 import *


@pytest.mark.parametrize('x,y,expected', {
    (0, -1, -math.pi / 2),
    (1, -1, -math.pi / 4),
    (1, 0, 0),
    (1, 1, math.pi / 4),
    (0, 1, math.pi / 2),
    (-1, 1, 3 * math.pi / 4),
    (-1, 0, math.pi),
    (-1, -1, 5 * math.pi/4)
})
def test_angle(x, y, expected):
    assert angle(x, y) == expected
