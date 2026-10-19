"""Abstract data classes that enable data manipulation with coordinates.

[TODO:description]
"""

from collections.abc import Generator, Iterator
from copy import copy
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

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
        """Does coordinate addition logic between vectors or tuples.

        Args:
            other: Vector or tuple that stores two coordinates of the same type.

        Returns:
            New Vector, with the coordinates storing the result of sum.
        """
        y, x = other
        return Vector(self.y + y, self.x + x)

    def __radd__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        return self + other

    def __mul__(self, other: N) -> "Vector[N]":
        return Vector(self.y * other, self.x * other)

    def __sub__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        y, x = other
        return Vector(self.y - y, self.x - x)

    def __rsub__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        y, x = other
        return Vector(y - self.y, x - self.x)

    def __eq__(self, other: object) -> Any:
        y, x = other
        return self.y == y and self.x == x


T = TypeVar("T")


class Cell(Generic[T]):
    def __new__(
        cls, y: int, x: int, ref: "Grid[T]", value: T | None = None
    ) -> "Cell[T]":
        if ref is not None:
            if ref.cant_reach(y, x):
                raise ValueError("Coordinates are not reachable")
            return super().__new__(cls)
        else:
            raise ValueError("ref cant be None")

    def __init__(self, y: int, x: int, ref: "Grid[T]", value: T | None = None) -> None:
        self._value = value  # should be set as first value
        self._grid = ref
        self.y, self.x = y, x
        # if not hasattr(value, '__dict__'):
        #     self._value = value
        #     return
        # for name, value in list(vars(value).items()):
        #     setattr(self, name, value)

    def __call__(self, y: int, x: int) -> "Cell[T] | None":
        if self._grid.cant_reach(y, x):
            return None
        return self._grid[y][x]

    def __iter__(self) -> Iterator[str]:
        yield from vars(self)

    def __add__(self, other: Vector[int] | tuple[int, int]) -> "Cell[T] | None":
        y_move, x_move = other
        return self(self.y + y_move, self.x + x_move)

    def __getattr__(self, name: str) -> Any:
        if name in dir(self):
            return self.__getattribute__(name)
        return getattr(self._value, name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_value" or name not in dir(self._value):
            return super().__setattr__(name, value)
        return setattr(self._value, name, value)

    def neighbour(self, other: Vector[int] | tuple[int, int]) -> "Cell[T] | None":
        return self + other

    @property
    def valid(self) -> bool:
        return True


class Grid(Generic[T]):
    def __init__(
        self,
        width: int,
        height: int,
        default: T | None = None,
        cell_class: type["Cell[T]"] = Cell[T],
    ) -> None:
        if width < 1 or height < 1:
            raise ValueError("Grid can't have zero/negative width or height")
        self._cell_class = cell_class
        self.default = default
        self.height = height
        self.width = width
        self._grid = [
            [self._cell_class(y, x, self, copy(default)) for x in range(self.width)]
            for y in range(self.height)
        ]
        self._cell = self._grid[0][0]

    def __iter__(self) -> Generator[Cell[T] | None, Any, None]:
        for y in range(self.height):
            for x in range(self.width):
                yield self.cell(y, x)

    @property
    def cell(self) -> Cell[T]:
        return self._cell

    @property
    def valid(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if not self.cell(y, x).valid:
                    return False
        return True

    def cant_reach(self, y: int, x: int) -> bool:
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def __getitem__(self, y: int) -> list[Cell[T]]:
        return self._grid[y]

    def row(self, y: int) -> Generator[Cell[T] | None, Any, None]:
        for index in range(self.width):
            yield self.cell(y, index)

    def column(self, x: int) -> Generator[Cell[T] | None, Any, None]:
        for index in range(self.height):
            yield self.cell(index, x)
