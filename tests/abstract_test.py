
import pytest

from submodules.abstract import *
from submodules.enums import Move, Wall


def test_vector():
    assert Vector(0, 3) * 3 == (0, 9)
    assert Vector(1, 2) == Vector(0, 2) + Vector(1, 0)
    assert Vector(3, 9) - Vector(1, 3) == Vector(2, 6)

def test_grid():
    with pytest.raises(ValueError):
        Grid(-3, -2, 0)
    with pytest.raises(TypeError):
        grid = Grid(2, 2, Wall.BLOCK)
    grid = Grid(2, 2)
    assert grid.valid == True
    for cell in grid.row(0):
        assert cell.y == 0
    for cell in grid.column(1):
        assert cell.x == 1
    grid_int = Grid(2, 2)
    assert len(list(grid_int)) == 4
    assert grid_int[0][0].y == 0
    assert grid_int[1][0].y == 1
    assert grid_int.cant_reach(10, 0) == True

def test_cell():
    with pytest.raises(ValueError):
        Cell(-2, -3, Grid(3, 2))
    grid = Grid(2, 2)
    cell = grid[0][0]
    assert cell + Move.RIGHT == cell(0, 1)
    assert cell + Move.RIGHT * 6 == None
    assert cell + Move.RIGHT * 2 == cell(0, 2)
    assert cell.valid == True


if __name__ == '__main__':
    test_grid()
    test_cell()
    test_vector()
