"""Abstract data classes that enable data manipulation with coordinates.

[TODO:description]
"""

from collections.abc import Generator, Iterable, Iterator
from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from typing_extensions import Self

N = TypeVar("N", int, float)


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


class Cell:
    """Stores y, x as coordinates, and reference to grid it belongs to."""

    def __init__(self, y: int, x: int, ref: "Grid") -> None:
        """Creates an instance of Cell only if Cell can be made.

        Args:
            y: Vertical coordinate.
            x: Horizontal coordinate.
            ref: Reference to the Grid this cell belongs to.

        Returns:
            Cell instance.

        Raises:
            ValueError: In case ref is None or coordinates are unreachable.
        """
        if ref is None:
            raise ValueError("ref cant be None")
        if ref.cant_reach(y, x):
            raise ValueError("Coordinates are not reachable")
        self._grid: Grid = ref
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
        return self._grid[y][x]

    def __iter__(self) -> Iterator[int]:
        """Unpack Cell coordinates.

        Returns:
            Iterator over y and x.
        """
        return iter([self.y, self.x])

    def __add__(self, other: Vector[int] | tuple[int, int]) -> Self | None:
        """Add coordinates and lookup a cell at that position.

        Args:
            other: Vector or tuple of ints.
            Its coordinates are used as an offset.

        Returns:
            Cell if it exists at resulting coordinates, None otherwise.
        """
        y_move, x_move = other
        return self(self.y + y_move, self.x + x_move)

    def neighbour(self, other: Vector[int] | tuple[int, int]) -> Self | None:
        """Same as __add__."""
        return self + other

    @property
    def valid(self) -> bool:
        """Validity of cell."""
        return True


class Grid:
    """Stores Cells. Has basic navigation and validation methods.

    Attributes:
        height: How many rows in the grid.
        width: How many columns in the grid.
    """

    def __init__(self, height: int, width: int, cell_class: type[Cell] = Cell) -> None:
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
        self._cell_class = cell_class
        self.height = height
        self.width = width
        self._grid = [
            [cell_class(y, x, self) for x in range(self.width)]
            for y in range(self.height)
        ]

    def __iter__(self) -> Generator[Cell]:
        """Iterate over Cells within Grid."""
        for y in range(self.height):
            for x in range(self.width):
                yield self._grid[y][x]

    @property
    def valid(self) -> bool:
        """Grid's validity."""
        for y in range(self.height):
            for x in range(self.width):
                if not self._grid[y][x].valid:
                    return False
        return True

    def cant_reach(self, y: int, x: int) -> bool:
        """Check if coordinates are unreachable."""
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def __getitem__(self, y: int) -> list[Cell]:
        """Makes possible to access cells using Grid[y][x] syntax."""
        return self._grid[y]

    def row(self, y: int) -> Generator[Cell]:
        """Yield a row within a Grid."""
        for index in range(self.width):
            yield self._grid[y][index]

    def column(self, x: int) -> Generator[Cell, Any, None]:
        """Yield a column within a Grid."""
        for index in range(self.height):
            yield self._grid[index][x]
