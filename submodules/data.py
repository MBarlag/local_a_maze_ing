from typing import Any
from dataclasses import dataclass, field
from enum import Enum, IntEnum, Flag, IntFlag
from functools import wraps

# TODO: think about rwriting methods to using Cell instead of y, x?
# could be something like maze.shell(Cell(3,2)) -> Cell
# or maze.break_wall(Cell(2,15), Walls.N)
# class Cell:
#     # use singleton?
#     # use it as a more readable access point
#     # to replace all of the coords x, y?
#     # implement addition against a tuple?
#     maze_ref: 'Maze' # only assigned one time

class Walls(Flag):
    W =     0b1000
    S =     0b0100
    E =     0b0010
    N =     0b0001
    EMPTY = 0b0000
    BLOCK = 0b1111        

    def opposite(self):
        opposites = {Walls.W: Walls.E,
                     Walls.E: Walls.W,
                     Walls.N: Walls.S,
                     Walls.S: Walls.N}
        return opposites.get(self, Walls.EMPTY)
    
    def __iter__(self):
        for wall in [Walls.W, Walls.S, Walls.E, Walls.N]:
            if wall in self:
                yield wall
            else: yield Walls.EMPTY


# TODO think if we even need low level here? maybe just maze is ok?
# TODO reeval if dataclass needed here
@dataclass(repr=False)
class Grid(list):
    width: int
    height: int
    # TODO make generic later
    default: Any

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

    def validate(self):
        for x in range(self.width):
            for y in range(self.height):
                self.validate_cell(y, x) # implement Cell interface?
        print("Valid!")


@dataclass
class Orientier:
    wall: Walls
    yd: int
    xd: int

class Direction(Orientier, Enum):
    LEFT = Walls.W, 0, -1
    DOWN = Walls.S, 1, 0
    RIGHT = Walls.E, 0, 1
    UP = Walls.N, -1, 0

    def __iter__(self):
        for i in range(len(Orientier.__dataclass_fields__)):
            yield self._value_[i]



class Maze(Grid):

    def __init__(self, width, height, default: Walls):
        super().__init__(width, height, default)

    def shell(self, y,  x):
        shell = Walls.BLOCK
        for wall, yd, xd in list(Direction):
            y_new = y = yd
            x_new = x + xd
            if self.cant_reach(y_new, x_new):
                continue
            if wall.opposite() not in self[y][x]:
                shell ^= wall
        return shell

    # can be offloaded to Cell(1,2).validate()?
    def validate_cell(self, y, x):
        # TODO: fix access outside of boundaries later
        if self[y][x] != self.shell(y, x):
            raise Exception("Maze not valid")
                
    # TODO: add validation of neighbors and breaking their walls too
    # can be offloaded to Cell(3,3).break_wall(to_break: Walls)
    def break_wall(self, y, x, to_break: Walls):
        if to_break in self[y][x]:
            self[y][x] ^= to_break
        for wall, yd, xd in list(Direction):
            if wall not in to_break \
                or self.cant_reach(y + yd, x + xd):
                continue

            
            
            
        else: raise ValueError("Walls requested dont exist")
        
a = Maze(3,3,Walls.BLOCK)
a.validate()
a.break_wall(0,0,Walls.S)
a.break_wall(1,0,Walls.N)
a.validate()
b = Maze(4, 1, Walls.BLOCK)
b.validate()