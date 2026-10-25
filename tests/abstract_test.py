from dataclasses import dataclass

import pytest

from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Move, Walls


def test_from_file() -> None:
    grid = Grid(7, 5, from_file="42.txt", map_char=lambda c: Walls(int(c, 16)))
    print(grid)
    assert grid[0, 0].value == Walls.BLOCK
    assert grid[2, 2].value == Walls.BLOCK
    assert grid[5, 2].value == Walls.BLOCK
    assert grid[4, 1].value == Walls.EMPTY
    assert grid[5, 3].value == Walls.EMPTY


def test_grid_add() -> None:
    result = Grid(2, 2, default=1) + Grid(2, 2, default=10)
    for cell in result:
        assert cell.value == 11


def test_grid_view() -> None:
    grid = Grid(7, 5, from_file="42.txt", map_char=lambda x: Walls(int(x, 16)))
    print(grid)
    print()
    view = grid.view(lambda x: x.value.value, x1=0, y1=2, x0=1, y0=0)
    view2 = grid.view(lambda x: x.as_vector)
    view3 = grid.view(lambda x: x.value, *(4, 3), *(2, 2))
    view4 = grid.view(lambda x: x.as_vector, *(4, 3), *(2, 2))
    print(view)
    print(view2)
    print(view3)
    print(view4)


def test_vector() -> None:
    assert Vector(0, 3) * 3 == (0, 9)
    assert Vector(1, 2) == Vector(0, 2) + Vector(1, 0)
    assert Vector(3, 9) - Vector(1, 3) == Vector(2, 6)


def test_grid() -> None:
    with pytest.raises(ValueError):
        Grid(-3, -2, default=9)
    assert Grid(4, 4, default=False).cell.value == False
    assert Grid(1, 1, default=True).cell.value == True
    a = Grid(4, 4, default=True)
    a[0, 0].value = True
    c = a[0, 1]
    assert c[0, 2] == c + Vector(0, 2)
    assert a.cell.value == True
    assert Grid(3, 3, default=3).cell.value == 3
    grid2 = Grid(2, 2)
    for cell in grid2.row(0):
        assert cell.y == 0
    for cell in grid2.column(1):
        assert cell.x == 1
    grid_int = Grid(2, 2, default=3, cell_class=Cell[int])
    assert len(list(grid_int)) == 4
    assert grid_int[0, 0].y == 0
    assert grid_int[1, 0].y == 0
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
    assert grid2.cell.value.x == 9
    assert grid2.cell.y == 0
    assert grid2.cell.z == True
    assert grid2.cell.name == "Hello Test"
    assert grid2.cell.number == -2222
    assert grid2.cell.value == val
    assert grid2.valid == True


def test_cell() -> None:
    with pytest.raises(ValueError):
        Cell(-2, -3, Grid(3, 3), value=None)
    grid = Grid(3, 3)
    cell = grid[0, 0]
    assert grid[1, 1] == cell[Move.RIGHT][Move.DOWN]
    assert cell + Move.RIGHT == cell[1, 0]
    assert cell.visit(*Move.RIGHT) == grid[1, 0]
    assert cell.visit(0, 1) == grid[0, 1]
    assert cell[Move.DOWN][Move.RIGHT] == grid[1, 1]
    assert grid[Move.RIGHT]
    assert cell + Move.RIGHT * 6 == None
    assert cell + Move.RIGHT * 2 == cell[2, 0]
    assert cell.valid == True
    assert cell[Move.LEFT + Move.RIGHT + Move.DOWN] == cell[0, 1]
    assert cell[Move.LEFT + Move.RIGHT] == cell[Move.NOWHERE]
    assert cell + Move.LEFT == None


if __name__ == "__main__":
    test_grid()
    test_cell()
    test_vector()
    test_cell_passthrough()
