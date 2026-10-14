
from typing import Any, Generic, TypeVar, Type
from dataclasses import dataclass
from copy import copy

N = TypeVar('N', int, float)

@dataclass
class Vector(Generic[N]):
    y: N
    x: N

    def __iter__(self):
        return iter([self.y, self.x])
    def __add__(self, other: Type['Vector[N]'] | tuple[N, N]):
        y, x = other
        return Vector(self.y + y, self.x + x)
    def __radd__(self, other: Type['Vector[N]'] | tuple[N, N]):
        return self + other
    def __mul__(self, other: N):
        return Vector(self.y * other, self.x  * other)
    def __sub__(self, other: Type['Vector[N]'] | tuple[N, N]):
        y, x = other
        return Vector(self.y - y, self.x - x)
    def __rsub__(self, other: Type['Vector[N]'] | tuple[N, N]):
        y, x = other
        return Vector(y - self.y, x - self.x)
    def __eq__(self, other: Type['Vector[N]'] | tuple[N, N]):
        y, x = other
        return self.y == y and self.x == x

T = TypeVar('T')
class Cell(Generic[T]):
    def __new__(cls, y: int, x: int, ref: 'Grid[T]', value: T = None):
        if ref is not None:
            if ref.cant_reach(y, x):
                raise ValueError("Coordinates are not reachable")
            return super().__new__(cls)
        else:
            raise ValueError("ref cant be None")
    def __init__(self, y: int, x: int, ref: 'Grid[T]', value: T = None):
        self._value = value # should be set as first value
        self._grid = ref
        self.y, self.x = y, x
        # if not hasattr(value, '__dict__'):
        #     self._value = value
        #     return
        # for name, value in list(vars(value).items()):
        #     setattr(self, name, value)

    def __call__(self, y: int, x: int) -> 'Cell[T]':
        if self._grid.cant_reach(y, x):
            return None
        return self._grid[y][x]

    def __iter__(self):
        for i in vars(self):
            yield i

    def __add__(self, other: Vector[int] | tuple[int, int]) -> 'Cell[T]':
        y_move, x_move = other
        return self(self.y + y_move, self.x + x_move)

    def __getattr__(self, name) -> Any:
        if name in dir(self):
            return self.__getattribute__(name)
        return getattr(self._value, name)

    def __setattr__(self, name, value):
        if name == '_value' or name not in dir(self._value):
            return super().__setattr__(name, value)
        return setattr(self._value, name, value)

    def neighbour(self, other: Vector[int] | tuple[int, int]) -> 'Cell[T]':
        return self + other

    @property
    def valid(self) -> bool:
        return True


class Grid(Generic[T]):

    _cell_class = Cell[T]

    def __init_subclass__(cls, cell_class : Type['Cell[T]'] = Cell[T], **kwargs):
        cls._cell_class = cell_class

    def __init__(self, width: int, height: int, default: T = None):
        if width < 1 or height < 1:
            raise ValueError("Grid can't have zero/negative width or height")
        self.default = default
        self.height = height
        self.width = width
        self._grid = [  [self._cell_class(y, x, self, copy(default)) 
                         for x in range(self.width)]
                      for y in range(self.height)   ]
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
