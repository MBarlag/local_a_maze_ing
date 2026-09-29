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

    def __neg__(self):
        opposites = {Walls.W: Walls.E,
                     Walls.E: Walls.W,
                     Walls.N: Walls.S,
                     Walls.S: Walls.N}
        return opposites[self]
    
    def __iter__(self):
        for wall in [Walls.W, Walls.S, Walls.E, Walls.N]:
            if wall in self:
                yield wall
            else: continue


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
 
    # TODO: move to higher level class
    # TODO: add validation of neighbors and breaking their walls too
    # def break_wall(self, y, x, to_break: Walls):
    #     if to_break in self[y][x]:
    #         self[y][x] ^= to_break
    #     else: raise ValueError("Walls requested dont exist")

    def neighbours(self, y,  x):
        coords = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        for x, y in coords:
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                continue
            yield self[y][x]
