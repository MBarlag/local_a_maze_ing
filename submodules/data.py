from collections.abc import Generator
from typing import cast

from typing_extensions import Self

from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Wall


class Room(Cell):

    def __init__(self, y: int, x: int, ref: Grid):
        super().__init__(y, x, ref)
        self.visited = False
        self.walls = Wall.BLOCK
        self.blocked = False

    @property
    def surrounded(self) -> Wall:
        surrounded = Wall.BLOCK
        for wall in Wall.BLOCK:
            neighbour = self + wall.direction
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                surrounded -= wall
        return surrounded

    @property
    def valid(self) -> bool:
        return self.walls == sum(self.surrounded)

    def break_wall(self, to_break: Wall) -> None:
        if to_break in self.walls:
            self.walls -= to_break
            neighbour = self + to_break.direction
            if neighbour is None:
                raise ValueError("Can't break borders of the maze")
            neighbour.walls -= to_break.opposite
        else:
            raise ValueError("Walls requested don't exist")
    
    def __call__(self, y: int, x: int) -> "Self | None":
        result = super().__call__(y, x)
        return cast(Self, result)
    def __add__(self, other: Vector[int] | tuple[int, int]) -> "Self":
        result = super().__add__(other)
        return cast(Self, result)
    def neighbour(self, other: Vector[int] | tuple[int, int]) -> "Self":
        result = super().neighbour(other)
        return cast(Self, result)

class Maze(Grid):

    def __init__(self, width: int, height: int, entry: Vector[int],
                 exit: Vector[int]) -> None:
        super().__init__(width, height, Room)
        self._set_entry(entry)
        self._set_exit(exit)

    def __iter__(self) -> Generator[Room]:
        result = super().__iter__()
        return cast(Generator[Room], result)

    def row(self, y: int) -> Generator[Room]:
        """Yield a row within a Grid."""
        result = super().row(y)
        return cast(Generator[Room], result)

    def column(self, x: int) -> Generator[Room]:
        """Yield a column within a Grid."""
        result = super().column(x)
        return cast(Generator[Room], result)
    

    @property
    def room(self) -> Room:
        result = self[0][0]
        return cast(Room, result)

    @property
    def entry(self) -> Vector[int]:
        return self._entry

    def _set_entry(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError("Coordinates are not reachable")
        self._entry = coord

    @property
    def exit(self) -> Vector[int]:
        return self._exit

    def _set_exit(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError("Coordinates are not reachable")
        self._exit = coord
