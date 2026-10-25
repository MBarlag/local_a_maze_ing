"""Abstract data classes that enable data manipulation with coordinates."""

from collections.abc import Callable, Generator, Iterable, Iterator
from copy import copy
from dataclasses import dataclass
from typing import Any, Generic, TypeVar, overload

from typing_extensions import Self

N = TypeVar("N", int, float)


@dataclass(frozen=True)
class Vector(Generic[N]):
    """2D Coordinate class, supports math operations.

    Supports vector operations like ==, +, - and * by singular value:
        > Vector(3, 4) + (2, 3) - Vector(2.5, 3.5) * 2 == Vector(0, 0)

    Supports tuple unpacking => x, y = Vector(4, 5)

    Attributes:
        x: Horizontal coordinate.
        y: Vertical coordinate.
    """

    x: N
    y: N

    def __str__(self) -> str:
        """Returns string representation of self."""
        return f"({self.x},{self.y})"

    def __iter__(self) -> Iterator[N]:
        """Iterate over x and y of the vector."""
        return iter([self.x, self.y])

    def __add__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Add two 2D vectors. (x, y) + (a, b) => Vector(x + a, y + b)."""
        x, y = other
        return Vector(self.x + x, self.y + y)

    def __radd__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Same as __add__."""
        return self + other

    def __mul__(self, other: N) -> "Vector[N]":
        """Multiply each value of the vector by other value."""
        return Vector(self.x * other, self.y * other)

    def __sub__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Subtract two 2D vectors. (x, y) - (a, b) => Vector(x - a, y - b)."""
        x, y = other
        return Vector(self.x - x, self.y - y)

    def __rsub__(self, other: "Vector[N] | tuple[N, N]") -> "Vector[N]":
        """Same as __sub__ but reversed."""
        x, y = other
        return Vector(x - self.x, y - self.y)

    def __eq__(self, other: object) -> bool:
        """Compare self to other.

        Args:
            other: Any object.

        Returns:
            True or False. If the can be tuple unpacked,
            will return true if the unpacked values are equal to respective
            values of the Vector: x and y.
        """
        if not isinstance(other, Iterable):
            return NotImplemented
        if len(list(other)) >= 2:
            x, y = list(other)[:2]
            if self.x == x and self.y == y:
                return True
        return False


_Data = TypeVar("_Data")
_Cell = TypeVar("_Cell", bound="Cell[Any]")


class Cell(Generic[_Data]):
    """Stores x, y coordinates and grid it belongs to."""

    @property
    def valid(self) -> bool:
        """Validity of cell."""
        return True

    @property
    def as_vector(self) -> Vector[int]:
        """Vector representation."""
        return Vector(*self)

    @property
    def value(self) -> _Data:
        """Data value."""
        return self._value

    @value.setter
    def value(self, value: _Data) -> None:
        self._value: _Data = value

    def visit(self, dx: int, dy: int) -> Self | None:
        """Add up coordinates and return the cell at the location or None."""
        new_position = self.as_vector + (dx, dy)
        if self._grid.cant_reach(*new_position):
            return None
        return self._grid[new_position]

    def __init__(
        self, x: int, y: int, ref: "Grid[_Data, Self]", value: _Data
    ) -> None:
        """Creates an instance of Cell only if Cell can be made.

        Args:
            x: Horizontal coordinate.
            y: Vertical coordinate.
            ref: Reference to the Grid this cell belongs to.
            value: Data to store.

        Returns:
            Cell instance.

        Raises:
            ValueError: In case ref is None or coordinates are unreachable.
        """
        if ref is None:
            raise ValueError("ref cant be None")
        if ref.cant_reach(x, y):
            raise ValueError("Coordinates are not reachable")
        self._value = value  # should be set as first value
        self._grid = ref
        self.x, self.y = x, y

    def __getitem__(self, offset: tuple[int, int] | Vector[int]) -> Self:
        """Get a cell by offset to self via self[dx, dy] or self[(dx, dy)].

        Args:
            offset: typle or Vector of dx, dy to shift current position by.

        Returns:
            Cell at the (x, y).

        Raises:
            IndexError: If out of bounds.
        """
        new_position = self.as_vector + offset
        if self._grid.cant_reach(*new_position):
            raise IndexError("Requested Cell is out of bounds")
        return self._grid[new_position]

    def __iter__(self) -> Iterator[int]:
        """Unpack Cell coordinates.

        Returns:
            Iterator over x and y.
        """
        return iter([self.x, self.y])

    def __add__(self, other: Vector[int] | tuple[int, int]) -> Self | None:
        """Add up coordinates and return the cell at the location.

        Args:
            other: Vector or tuple of ints.
            Its coordinates are used as an offset.

        Returns:
            Cell if it exists at resulting coordinates, None otherwise.
        """
        return self.visit(*other)

    def __getattr__(self, name: str) -> Any:
        """Get Attribute from Data. Except _grid, x, y, _value from Cell."""
        if name in dir(self):
            return self.__getattribute__(name)
        return getattr(self._value, name)

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute on the stored data, or else on the cell."""
        if name == "_value" or name not in dir(self._value):
            return super().__setattr__(name, value)
        return setattr(self._value, name, value)


class Grid(Generic[_Data, _Cell]):
    """Stores _Cells with _Data. Has basic navigation and validation methods.

    Access elements via grid[x, y].
    """

    @overload
    def __init__(
        self: "Grid[Any, Cell[Any]]",
        width: int,
        height: int,
    ) -> None: ...

    @overload
    def __init__(
        self: "Grid[_Data, Cell[_Data]]",
        width: int,
        height: int,
        *,
        default: _Data,
    ) -> None: ...

    @overload
    def __init__(
        self: "Grid[_Data, Cell[_Data]]",
        width: int,
        height: int,
        *,
        from_file: str,
        map_char: Callable[[str], _Data],
    ) -> None: ...

    @overload
    def __init__(
        self,
        width: int,
        height: int,
        *,
        default: _Data,
        cell_class: type[_Cell],
    ) -> None: ...

    @overload
    def __init__(
        self,
        width: int,
        height: int,
        *,
        default: _Data,
        cell_class: type[_Cell],
        from_file: str,
        map_char: Callable[[str], _Data],
    ) -> None: ...

    def __init__(
        self,
        width: int,
        height: int,
        *,
        default: Any = None,
        cell_class: Any = None,
        from_file: str | None = None,
        map_char: Callable[[str], _Data] | None = None,
    ) -> None:
        """Create a Grid of _Cells containing _Data.

        Args:
            width: How many columns.
            height: How many rows.
            default: Default data to store.
            cell_class: Class of Grid's elements. Is bound to Cell[_Data].
            from_file: Filename to init the Grid from.
            key: Function that maps each character of file to _Data.

        Raises:
            ValueError: If dimensions are invalid.
        """
        if width < 1 or height < 1:
            raise ValueError(
                f"{type(self).__name__} can't have \
                zero/negative width or height"
            )
        self._cell_class: type[Any] = cell_class or Cell
        self.default: _Data = default
        self.width: int = width
        self.height: int = height

        self._grid: list[list[_Cell]] = [
            [
                self._cell_class(x, y, self, copy(self.default))
                for y in range(self.height)
            ]
            for x in range(self.width)
        ]
        self._map_char = map_char
        self._from_file = from_file
        if from_file and map_char:
            self.load(from_file, map_char)

    def load(
        self,
        filename: str | None = None,
        map_char: Callable[[str], _Data] | None = None,
    ) -> None:
        """Loads grid from file, maps each character to element using map_char.

        File should have same dimensions or bigger than the grid.

        Args:
            filename: Name of the file to load from.
            map_char: Function that takes one str parameter and returns _Data.

        Raises:
            ValueError: If no filename or map_char could be found.
            IndexError: If file doesnt have correct dimensions.
        """
        from_file = filename or self._from_file
        map_character = map_char or self._map_char
        if not from_file or not map_character:
            raise ValueError("No filename or map_char could be found.")
        with open(from_file, "r", encoding="utf-8") as f:
            for y in range(self.height):
                line = f.readline()
                for x in range(self.width):
                    self[x, y].value = map_character(line[x])

    R = TypeVar("R")

    def view(
        self,
        viewer: Callable[[_Cell], R],
        x1: int = 0,
        y1: int = 0,
        x0: int = 0,
        y0: int = 0,
    ) -> "Grid[R, Cell[R]]":
        """Apply a viewer function to each cell and save result to new Grid."""
        if not x1:
            x1 = self.width - 1
        if not y1:
            y1 = self.height - 1
        width = x1 - x0 + 1
        height = y1 - y0 + 1
        result = Grid(width, height)
        for result_cell in result:
            offset = result_cell.as_vector
            origin = self[x0, y0]
            result_cell.value = viewer(origin[offset])
        return result

    def __iter__(self) -> Generator[_Cell]:
        """Iterate over Cells within Grid."""
        for x in range(self.width):
            for y in range(self.height):
                yield self[x, y]

    def __str__(self) -> str:
        """Returns str(self)."""
        result = ""
        for y in range(self.height):
            line = (
                "[ "
                + " | ".join(str(cell.value) for cell in self.row(y))
                + " ]\n"
            )
            result += line
        return result

    @property
    def cell(self) -> _Cell:
        """First Cell of Grid."""
        return self[0, 0]

    def __add__(self, other: "Grid[Any, _Cell]") -> "Grid[Any, _Cell]":
        """Adds two grids values together, cell by cell."""
        result = Grid(
            self.width, self.height, default=None, cell_class=other._cell_class
        )
        for result_cell, cell, other_cell in zip(result, self, other):
            result_cell.value = cell.value + other_cell.value
        return result

    @property
    def valid(self) -> bool:
        """Grid's validity."""
        for cell in self:
            if not cell.valid:
                return False
        return True

    def cant_reach(self, x: int, y: int) -> bool:
        """Check if coordinates are unreachable."""
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    def __getitem__(self, coords: tuple[int, int] | Vector[int]) -> _Cell:
        """self[x, y]. Get Cell at x,y absolute location within the Grid."""
        x, y = coords
        return self._grid[x][y]

    def row(self, y: int) -> Generator[_Cell]:
        """Yield a row within a Grid."""
        for index in range(self.width):
            yield self[index, y]

    def column(self, x: int) -> Generator[_Cell]:
        """Yield a column within a Grid."""
        for index in range(self.height):
            yield self[x, index]
