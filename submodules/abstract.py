
from typing import Any, Generic, TypeVar, Type
from dataclasses import dataclass

@dataclass
class Vector:
    y: int
    x: int

    def __iter__(self):
        return iter([self.y, self.x])
    def __add__(self, other: Type['Vector'] | tuple[int, int]):
        y, x = other
        return Vector(self.y + y, self.x + x)
    def __radd__(self, other: Type['Vector'] | tuple[int, int]):
        return self + other
    def __mul__(self, other: int):
        return Vector(self.y * other, self.x  * other)
    def __sub__(self, other: Type['Vector'] | tuple[int, int]):
        y, x = other
        return Vector(self.y - y, self.x - x)
    def __rsub__(self, other: Type['Vector'] | tuple[int, int]):
        y, x = other
        return Vector(y - self.y, x - self.x)
    def __eq__(self, other: Type['Vector'] | tuple[int, int]):
        y, x = other
        return self.y == y and self.x == x

T = TypeVar('T')


class Cell(Generic[T]):
    def __new__(cls, y: int, x: int, data: T, ref: 'Grid[T]'):
        if ref is not None and data is not None:
            if ref.cant_reach(y, x):
                raise ValueError("Coordinates are not reachable")
            return super().__new__(cls)
        else:
            raise ValueError("ref and default cant be None")

    def __init__(self, y: int, x: int, data: T, ref: 'Grid[T]'):
        self._grid = ref
        self._data = data
        self.y, self.x = y, x

    def __call__(self, y: int, x: int) -> 'Cell[T]':
        if self._grid.cant_reach(y, x):
            return None
        return self._grid[y][x]

    def __iter__(self):
        for i in vars(self):
            yield i

    def __add__(self, other: Vector | tuple[int, int]) -> 'Cell[T]':
        y_move, x_move = other
        return self(self.y + y_move, self.x + x_move)

    def __getattr__(self, name) -> Any:
        if name in dir(self):
            return dir(self)[name]
        return getattr(self._data, name)

    def neighbour(self, other: Vector | tuple[int, int]) -> 'Cell[T]':
        return self + other

    @property
    def valid(self) -> bool:
        return True


class Grid(Generic[T]):

    def __new__(cls, width: int, height: int, default: T):
        if width < 1 or height < 1:
            raise ValueError("Grid can't have zero/negative width or height")
        return super().__new__(cls)

    def __init__(self, width: int, height: int, default: T):
        self.default = default
        self.height = height
        self.width = width
        self._grid = [[Cell(y, x, default, self) for x in range(self.width)]
                      for y in range(self.height)]
        self._cell = self._grid[0][0]

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield self.cell(y, x)

    @property
    def cell(self):
        return self._cell

    @property
    def valid(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if not self.cell(y, x).valid:
                    return False
        return True

    def cant_reach(self, y: int, x: int):
        return (x < 0 or y < 0
                or x >= self.width
                or y >= self.height)

    def __getitem__(self, y: int) -> list[Cell[T]]:
        return self._grid[y]

    def row(self, y: int):
        for index in range(self.width):
            yield self.cell(y, index)

    def column(self, x: int):
        for index in range(self.height):
            yield self.cell(index, x)

