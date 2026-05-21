import pytest

from game import *

def test_coordinate_init():
    coordinate = Coordinate( 1, 2 )
    assert coordinate.x == 1
    assert coordinate.y == 2

def test_coordinate_repr():
    coordinate = Coordinate( 2, 3 )
    assert repr(coordinate) == "(2,3)"