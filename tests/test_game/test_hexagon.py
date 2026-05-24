import pytest

from game import *

def test_hexagon_init():
    coordinate = [1,2]
    hexagon = Hexagon(coordinate)
    assert hexagon.coordinate is coordinate

def test_hexagon_repr():
    coordinate = [2,3]
    hexagon = Hexagon(coordinate)
    assert repr(hexagon) == "(2,3)"