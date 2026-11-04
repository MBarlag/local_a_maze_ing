from functools import reduce

from mazegen.enums import *


def test_move_add():
    assert (
        reduce(Vector.__add__, [Step.LEFT, Step.RIGHT, Step.UP, Step.DOWN])
        == Step.NOWHERE
    )
    assert Step.LEFT + Step.RIGHT == Step.NOWHERE


def test_move_mul():
    assert Step.RIGHT * 6 == Vector(6, 0)


def test_move_eq():
    assert Step.RIGHT == (1, 0)
    assert Step.RIGHT == Vector(1, 0)
    assert Step.LEFT == Vector(-1, 0)
    assert Step.LEFT == (-1, 0)
