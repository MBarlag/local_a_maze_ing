from enums import *
from functools import reduce
import pytest

def test_move_add():
    assert reduce(Vector.__add__, [Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN]) == Move.NOWHERE
    assert Move.LEFT + Move.RIGHT == Move.NOWHERE

def test_move_mul():
    assert Move.RIGHT * 6 == Vector(0, 6)

def test_move_eq():
    assert Move.RIGHT == (0, 1)
    assert Move.RIGHT == Vector(0, 1)
    assert Move.LEFT == Vector(0, -1)
    assert Move.LEFT == (0, -1)
