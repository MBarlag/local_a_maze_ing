from abstract import *
from enums import Wall, Move
from functools import reduce
import pytest

def test_vector():
    assert Vector(0, 3) * 3 == (0, 9)
    assert Vector(1, 2) == Vector(0, 2) + Vector(1, 0)
    assert Vector(3, 9) - Vector(1, 3) == Vector(2, 6)

def test_grid():
    with pytest.raises(ValueError):
        Grid(-3, -2, 0)
    grid = Grid(2, 2, Wall.BLOCK)
    assert grid.valid == True
    for cell in grid.row(0):
        assert cell.y == 0
    for cell in grid.column(1):
        assert cell.x == 1
    grid_int = Grid(2, 2, 0)
    assert grid_int.cell._value == 0
    assert grid.cell.opposite == Wall.EMPTY
    assert grid.cell.__class__ == Cell

def test_cell():
    with pytest.raises(ValueError):
        Cell(-2, -3, Grid(3, 2, 0))
    grid = Grid(2, 2, Wall.BLOCK)
    assert grid.cell + Move.RIGHT == grid.cell(0, 1)
    assert grid.cell + Move.RIGHT * 6 == None
    assert grid.cell + Move.RIGHT * 2 == grid.cell(0, 2)
    assert grid.cell.valid == True


if __name__ == '__main__':
    test_grid()
    test_cell()
    test_vector()
