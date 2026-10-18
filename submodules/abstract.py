"""Abstract data classes that enable data manipulation with coordinates.

[TODO:description]
"""

from collections.abc import Generator, Iterable, Iterator
from dataclasses import dataclass
from typing import Any, Generic, Self, TypeVar

N = TypeVar("N", int, float)


@dataclass
class Vector(Generic[N]):
    """Coordinate class, stores y and x in it.

    Supports vector operations like ==, +, - and * by singular value:
        > Vector(3, 4) + (2, 3) - Vector(2.5, 3.5) * 2 == Vector(0, 0)

    Supports tuple unpacking => y, x = Vector(4, 5)

    Attributes:
        y: height dimension
        x: width dimension
    """

    y: N
    x: N

    def __iter__(self) -> Iterator[N]:
        """Iterate over y and x of the vector."""
        return iter([self.y, self.x])

    def __add__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Add two 2D vectors. (x, y) + (a, b) => Vector(x + a, y + b)."""
        y, x = other
        return Vector(self.y + y, self.x + x)

    def __radd__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Same as __add__."""
        return self + other

    def __mul__(self, other: N) -> "Vector[N]":
        """Multiply each value of the vector by other value."""
        return Vector(self.y * other, self.x * other)

    def __sub__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Subtract two 2D vectors. (x, y) - (a, b) => Vector(x - a, y - b)."""
        y, x = other
        return Vector(self.y - y, self.x - x)

    def __rsub__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Same as __sub__ but reversed."""
        y, x = other
        return Vector(y - self.y, x - self.x)

    def __eq__(self, other: object) -> bool:
        """Compare self to other.

        Args:
            other: Any object.

        Returns:
            True or False. If the can be tuple unpacked,
            will return true if the unpacked values are equal to respective
            values of the Vector: y and x.
        """
        if not isinstance(other, Iterable):
            return NotImplemented
        if len(list(other)) >= 2:
            y, x = list(other)[:2]
            if self.y == y and self.x == x:
                return True
        return False


class Cell:

    def __new__(cls, y: int, x: int, ref: "Grid") -> Self:
        if ref is not None:
            if ref.cant_reach(y, x):
                raise ValueError("Coordinates are not reachable")
            return super().__new__(cls)
        else:
            raise ValueError("ref cant be None")

    def __init__(self, y: int, x: int, ref: "Grid") -> None:
        self._grid: Grid = ref
        self.y, self.x = y, x

    def __call__(self, y: int, x: int) -> "Cell | None":
        if self._grid.cant_reach(y, x):
            return None
        return self._grid[y][x]

    def __iter__(self) -> Iterator[str]:
        yield from vars(self)

    def __add__(self, other: Vector[int] | tuple[int, int]) -> "Cell | None":
        y_move, x_move = other
        return self(self.y + y_move, self.x + x_move)

    def neighbour(self, other: Vector[int] | tuple[int, int]) -> "Cell | None":
        return self + other

    @property
    def valid(self) -> bool:
        return True


class Grid:

    def __init__(self,
                 width: int,
                 height: int,
                 cell_class: type[Cell] = Cell) -> None:
        if width < 1 or height < 1:
            raise ValueError("Grid can't have zero/negative width or height")
        self._cell_class = cell_class
        self.height = height
        self.width = width
        self._grid = [[cell_class(y, x, self) for x in range(self.width)]
                      for y in range(self.height)]

    def __iter__(self) -> Generator[Cell, Any, None]:
        for y in range(self.height):
            for x in range(self.width):
                yield self._grid[y][x]

    @property
    def valid(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if not self._grid[y][x].valid:
                    return False
        return True

    def cant_reach(self, y: int, x: int) -> bool:
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def __getitem__(self, y: int) -> list[Cell]:
        return self._grid[y]

    def row(self, y: int) -> Generator[Cell, Any, None]:
        for index in range(self.width):
            yield self._grid[y][index]

    def column(self, x: int) -> Generator[Cell, Any, None]:
        for index in range(self.height):
            yield self._grid[index][x]
