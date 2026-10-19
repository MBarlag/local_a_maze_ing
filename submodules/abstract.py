"""Abstract data classes that enable data manipulation with coordinates.

[TODO:description]
"""

from collections.abc import Generator, Iterable, Iterator
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, cast, overload
from copy import copy
from typing_extensions import Self

N = TypeVar("N", int, float)
# CLike = TypeVar("CLike", bound="Cell")


@dataclass
class Vector(Generic[N]):
    """2D Coordinate class, supports math operations.

    Supports vector operations like ==, +, - and * by singular value:
        > Vector(3, 4) + (2, 3) - Vector(2.5, 3.5) * 2 == Vector(0, 0)

    Supports tuple unpacking => y, x = Vector(4, 5)

    Attributes:
        y: Vertical coordinate.
        x: Horizontal coordinate.
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


T = TypeVar("T")
C = TypeVar("C", bound="Cell[Any]")


class Cell(Generic[T]):
    """Stores y, x as coordinates, and reference to grid it belongs to."""

    def __init__(
        self, y: int, x: int, 
        ref: "Grid[T, Self]", 
        value: T | None = None
    ) -> None:
        """Creates an instance of Cell only if Cell can be made.

        Args:
            y: Vertical coordinate.
            x: Horizontal coordinate.
            ref: Reference to the Grid this cell belongs to.
            value: Data to store.

        Returns:
            Cell instance.

        Raises:
            ValueError: In case ref is None or coordinates are unreachable.
        """
        if ref is None:
            raise ValueError("ref cant be None")
        if ref.cant_reach(y, x):
            raise ValueError("Coordinates are not reachable")
        self._value = value  # should be set as first value
        self._grid = ref
        self.y, self.x = y, x

    def __call__(self, y: int, x: int) -> Self | None:
        """Visit another cell within a grid.

        Args:
            y: Vertical coordinate.
            x: Horizontal coordinate.

        Returns:
            Cell at the (y, x).
        """
        if self._grid.cant_reach(y, x):
            return None
        return self._grid[y, x]

    def __iter__(self) -> Iterator[int]:
        """Unpack Cell coordinates.

        Returns:
            Iterator over y and x.
        """
        return iter([self.y, self.x])

    def __add__(self, other: Vector[int] | tuple[int, int]) -> Self | None:
        """Jump to position and return cell if exists.

        Args:
            other: Vector or tuple of ints.
            Its coordinates are used as an offset.

        Returns:
            Cell if it exists at resulting coordinates, None otherwise.
        """
        y_move, x_move = other
        return self.__call__(self.y + y_move, self.x + x_move)

    def __getattr__(self, name: str) -> Any:
        """Get attribute from Cell or it's Data."""
        if name in dir(self):
            return self.__getattribute__(name)
        return getattr(self._value, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute of Cell or it's Data."""
        if name == "_value" or name not in dir(self._value):
            return super().__setattr__(name, value)
        return setattr(self._value, name, value)

    def neighbour(self, other: Vector[int] | tuple[int, int]) -> Self | None:
        """Same as __add__."""
        return self + other

    @property
    def valid(self) -> bool:
        """Validity of cell."""
        return True


class Grid(Generic[T, C]):
    """Stores Cells. Has basic navigation and validation methods.

    Attributes:
        height: How many rows in the grid.
        width: How many columns in the grid.
    """
    @overload
    def __init__(self, height: int, width: int, default: T | None = None) -> None: ...
    @overload
    def __init__(
        self, height: int, width: int, default: T | None = None, *, cell_class: type[C]
    ) -> None: ...
    def __init__(
        self,
        height: int,
        width: int,
        default: T | None = None,
        *,
        cell_class: type[Any] | None = None,
    ):
        """Create a Grid of Cells.

        Args:
            height: How many rows.
            width: How many columns.
            cell_class: Class of Grid's elements.
                Must accept Grid in its constructor.

        Raises:
            ValueError: If dimensions are invalid.
        """
        if width < 1 or height < 1:
            raise ValueError("Grid can't have zero/negative width or height")
        self._cell_class: type[Any] = cell_class or Cell
        self.default = default
        self.height = height
        self.width = width
        self._grid: list[list[C]] = [
            [self._cell_class(y, x, self, copy(default)) for x in range(self.width)]
            for y in range(self.height)
        ]

    def __iter__(self) -> Generator[C]:
        """Iterate over Cells within Grid."""
        for y in range(self.height):
            for x in range(self.width):
                yield self[y, x]

    @property
    def cell(self) -> C:
        """First Cell of Grid."""
        return self[0, 0]

    @property
    def valid(self) -> bool:
        """Grid's validity."""
        for y in range(self.height):
            for x in range(self.width):
                if not self[y, x].valid:
                    return False
        return True

    def cant_reach(self, y: int, x: int) -> bool:
        """Check if coordinates are unreachable."""
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def __getitem__(self, coords: tuple[int, int]) -> C:
        y, x = coords
        return self._grid[y][x]

    def row(self, y: int) -> Generator[C]:
        """Yield a row within a Grid."""
        for index in range(self.width):
            yield self[y, index]

    def column(self, x: int) -> Generator[C]:
        """Yield a column within a Grid."""
        for index in range(self.height):
            yield self[index, x]
