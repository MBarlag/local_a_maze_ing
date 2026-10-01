from typing import Any, Generic, TypeVar
from dataclasses import dataclass, field
from enum import Enum, IntEnum, Flag, IntFlag
from functools import wraps
from collections.abc import Callable, Iterable, Iterator
from abc import ABC


class Move(Enum):
    LEFT    = (0, -1)
    DOWN    = (1, 0)
    RIGHT   = (0, 1)
    UP      = (-1, 0)
    NOWHERE = (0, 0)

class Wall(Flag):
    W =     0b1000
    S =     0b0100
    E =     0b0010
    N =     0b0001
    EMPTY = 0b0000
    BLOCK = 0b1111


    @property
    def opposite(self):
        opposites = \
            {Wall.W: Wall.E,
            Wall.E: Wall.W,
            Wall.N: Wall.S,
            Wall.S: Wall.N}
        return opposites.get(self, Wall.EMPTY)
    
    def __iter__(self):
        for wall in [Wall.W, Wall.S, Wall.E, Wall.N]:
            if wall in self:
                yield wall
            else: yield Wall.EMPTY
    
    def __add__(self, other: Flag | int):
        return self | Wall(other)
    def __radd__(self, other: Flag | int):
            return self | Wall(other)
    def __sub__(self, other: Flag | int):
        return self ^ Wall(other)
    def __rsub__(self, other: Flag | int):
        return Wall(other) ^ self

T = TypeVar('T')
class Grid(Generic[T]):

    _cell: '_Cell'
    def __init__(self, width: int, height: int, default: Any):
        self.default = default
        self.width = width
        self.height = height
        super().__init__([[default for x in range(self.width)] 
                          for y in range(self.height)])

    @property
    def valid(self) -> bool:
        for y in self.height:
            for x in self.width:
                self._cell
    
    def cant_reach(self, y: int, x: int):
        return (x < 0 or y < 0 \
            or x >= self.width \
            or y >= self.height)
    
    def row(self, n):
        for index in range(len(self)):
            yield self[n][index]

    def column(self, n):
        for index in range(len(self)):
            yield self[index][n]


class _Cell(Generic[T]):

    def __new__(cls, ref: Grid[T]):
        if ref:
            return cls(ref)
        else: raise ValueError("Grid is None")
    def __init__(self, ref: Grid[T]):
        self._grid = ref
        setattr(self, T.__name__.lower(), self._get_t)
        self(y=0, x=0)

    def __call__(self, y: int, x: int) -> '_Cell[T]':
        if self._grid.cant_reach(y, x):
            return None
        else: 
            self.y, self.x = y, x
            return self

    def __iter__(self):
        for i in vars(self):
            yield i

    def __add__(self, other: tuple[int, int]) -> '_Cell[T]':
        y_move, x_move = other
        return self(self.y + y_move, self.x + x_move)

    def neighbour(self, other: tuple[int, int]) -> '_Cell[T]':
        return self + other

    @property
    def _get_t(self) -> T:
        y, x = self.y, self.x
        return self._grid[y][x]

    @property
    def valid(self) -> bool:
        pass



class Room(Grid.Cell):
    @property
    def surrounded(self) -> Wall:
        surrounded = Wall.BLOCK
        for wall, move in list(zip(Wall, Move)):
            neighbour = self + move
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                surrounded -= wall
        return surrounded

    # TODO: add validation of neighbors and breaking their walls too
    def break_wall(self, y, x, to_break: Wall):
        if to_break in self[y][x]:
            self[y][x] -= to_break
        for wall, yd, xd in list(zip(Wall, Move)):
            if wall not in to_break \
                or self.cant_reach(y + yd, x + xd):
                continue
        else: raise ValueError("Walls requested dont exist")

class Maze(Grid):
    _cell: Cell
    
    def __init__(self, width, height, default):
        super().__init__(width, height, default)
        self._cell(self)
    
    
    def validate(self):
        for x in range(self.width):
            for y in range(self.height):
                self.validate_cell(y, x) # implement Cell interface?
        print("Valid!")


a = Maze(3,3,Wall.BLOCK)
a.validate()
a.break_wall(0,0,Wall.S)
a.break_wall(1,0,Wall.N)
a.validate()
b = Maze(4, 1, Wall.BLOCK)
b.validate()