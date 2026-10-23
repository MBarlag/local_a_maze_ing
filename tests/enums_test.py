from functools import reduce

from submodules.enums import *


def test_move_add():
    assert (
        reduce(Vector.__add__, [Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN])
        == Move.NOWHERE
    )
    assert Move.LEFT + Move.RIGHT == Move.NOWHERE


def test_move_mul():
    assert Move.RIGHT * 6 == Vector(6, 0)


def test_move_eq():
    assert Move.RIGHT == (1, 0)
    assert Move.RIGHT == Vector(1, 0)
    assert Move.LEFT == Vector(-1, 0)
    assert Move.LEFT == (-1, 0)
