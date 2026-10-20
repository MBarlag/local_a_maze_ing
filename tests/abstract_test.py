from dataclasses import dataclass

import pytest

from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Move


def test_vector() -> None:
    assert Vector(0, 3) * 3 == (0, 9)
    assert Vector(1, 2) == Vector(0, 2) + Vector(1, 0)
    assert Vector(3, 9) - Vector(1, 3) == Vector(2, 6)


def test_grid() -> None:
    with pytest.raises(ValueError):
        Grid(-3, -2, 9)
    assert Grid(3, 3, False).cell.value == False
    assert Grid(1, 1, True).cell.value == True
    a = Grid(1, 3, True)
    assert a.cell.value == True
    assert Grid(3, 3, 3).cell.value == 3
    grid2 = Grid(2, 2)
    for cell in grid2.row(0):
        assert cell.y == 0
    for cell in grid2.column(1):
        assert cell.x == 1
    grid_int = Grid(2, 2, 3, cell_class=Cell[int])
    assert len(list(grid_int)) == 4
    assert grid_int[0, 0].y == 0
    assert grid_int[1, 0].y == 1
    assert grid_int.cant_reach(10, 0) == True


def test_cell_passthrough() -> None:

    grid2 = Grid(2, 2)
    assert grid2.cell.value == None
    grid2.cell.value = 5
    assert grid2.cell.value == 5

    @dataclass
    class T:
        x: int = 9
        y: int = 10
        z: bool = True
        name: str = "Hello Test"
        number: int = -2222

    val = T()
    grid2.cell.value = val
    assert grid2.cell.x == 0
    assert grid2.cell.y == 0
    assert grid2.cell.z == True
    assert grid2.cell.name == "Hello Test"
    assert grid2.cell.number == -2222
    assert grid2.cell.value == val
    assert grid2.valid == True


def test_cell() -> None:
    with pytest.raises(ValueError):
        Cell(-2, -3, Grid(3, 3), None)
    grid = Grid(3, 3)
    cell = grid[0, 0]
    assert grid[1, 1] == cell[Move.RIGHT][Move.DOWN]
    assert cell + Move.RIGHT == cell[0, 1]
    assert cell.visit(*Move.RIGHT) == grid[0, 1]
    assert cell.visit(0, 1) == grid[0, 1]
    assert cell[Move.DOWN][Move.RIGHT] == grid[1, 1]
    assert grid[Move.RIGHT]
    assert cell + Move.RIGHT * 6 == None
    assert cell + Move.RIGHT * 2 == cell[0, 2]
    assert cell.valid == True
    assert cell[Move.LEFT + Move.RIGHT + Move.DOWN] == cell[1, 0]
    assert cell[Move.LEFT + Move.RIGHT] == cell[Move.NOWHERE]
    assert cell + Move.LEFT == None


if __name__ == "__main__":
    test_grid()
    test_cell()
    test_vector()
    test_cell_passthrough()
