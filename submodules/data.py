from typing import Any
from dataclasses import dataclass, field
from enum import Enum, IntEnum, Flag, IntFlag
from functools import wraps
from collections.abc import Callable, Iterable, Container


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


# TODO think if we even need low level here? maybe just maze is ok?
# TODO reeval if dataclass needed here
@dataclass(repr=False)
class Grid(list):
    width: int
    height: int
    # TODO make generic later
    default: Any
    _elem_view: Callable | Iterable | Container

    def __init__(self, width: int, height: int, default: Any):
        self.width = width
        self.height = height
        super().__init__([[default for x in range(self.width)] 
                          for y in range(self.height)])
    
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


# TODO: think about rwriting methods to using Cell instead of y, x?
# could be something like maze.shell(Cell(3,2)) -> Cell
# or maze.break_wall(Cell(2,15), Walls.N)
class Cell:
    _maze_ref: Grid = None # only assigned one time

    def __add__(self, other: tuple[int, int]) -> 'Cell':
        y_move, x_move = other
        return Cell(self.y + y_move, self.x + x_move)

    @property
    def walls(self) -> Wall:
        y, x = self.y, self.x
        if not self._maze_ref:
            raise Exception("Cell view is not linked to maze")
        return self._maze_ref[y][x]

    def __contains__(self, item: Wall):
        return item in self.walls

    @classmethod
    def __call__(cls, ref: Grid):
        if not cls._maze_ref:
            cls._maze_ref = ref
        else:
            raise Exception("Cell already is linked to an existing Maze")

    @classmethod
    def __new__(cls, y: int, x: int) -> 'Cell' | None:
        if cls._maze_ref.cant_reach(y, x):
            return None
        else: return cls(y, x)

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    @property
    def valid(self):
        return self.walls != sum(self.surrounded)


    # use singleton?
    # use it as a more readable access point
    # to replace all of the coords x, y?
    # implement addition against a tuple?

class Room(Cell):
    @property
    def surrounded(self) -> Wall:
        surrounded = Wall.BLOCK
        for wall, move in list(zip(Wall, Move)):
            neighbour = self + move
            if neighbour is None:
                continue
            if wall.opposite not in neighbour:
                surrounded ^= wall
        return surrounded

    # TODO: add validation of neighbors and breaking their walls too
    def break_wall(self, y, x, to_break: Wall):
        if to_break in self[y][x]:
            self[y][x] ^= to_break
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