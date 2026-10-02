
from typing import Any, Generic, TypeVar

T = TypeVar('T')

class Cell(Generic[T]):
    def __new__(cls, y: int, x: int, data: T, ref: 'Grid[T]'):
        if ref and data:
            if ref.cant_reach(y, x):
                return None
            return cls(y, x, data, ref)
        else: raise AttributeError("ref and default cant be None")

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

    def __add__(self, other: tuple[int, int]) -> 'Cell[T]':
        y_move, x_move = other
        return self(self.y + y_move, self.x + x_move)

    def __getattr__(self, name) -> Any:
        y, x = self.y, self.x
        return getattr(self.data, name)

    def neighbour(self, other: tuple[int, int]) -> 'Cell[T]':
        return self + other

    @property
    def valid(self) -> bool:
        pass


class Grid(Generic[T]):


    def __init__(self, width: int, height: int, default: T):
        self.default = default
        self.height = height
        self.width = width
        self._grid = [[Cell(y, x, default, self) for x in range(self.width)] 
                          for y in range(self.height)]
        self._cell = self._grid[0][0]

    def __iter__(self):
        yield 
    
    def __getitem__(self, y: int) -> list[Cell[T]]:
        return self._grid[y]

    def __iter__(self):
        for y in self.height:
            for x in self.width:
                yield self._cell(y, x)

    @property
    def cell(self):
        return self._cell
    
    @property
    def valid(self) -> bool:
        for y in self.height:
            for x in self.width:
                if not self._cell(y, x).valid:
                    return False
        return True
    
    def cant_reach(self, y: int, x: int):
        return (x < 0 or y < 0 \
            or x >= self.width \
            or y >= self.height)
    
    def row(self, y: int):
        for index in range(len(self)):
            yield self._cell(y, index)

    def column(self, x: int):
        for index in range(len(self)):
            yield self._cell(index, x)
