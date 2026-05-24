import pytest

from game import *

def test_game_init():
    rm = ResourceManager()
    gc = GameController( rm )

