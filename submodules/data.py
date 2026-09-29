from typing import Any
from dataclasses import dataclass, field
from enum import Enum, IntEnum, Flag, IntFlag
from functools import wraps
# @dataclass
# class RoomSetup:
#     walls: list[str] = field(default_factory=list)

class Walls(Flag):
    W =     0b1000
    S =     0b0100
    E =     0b0010
    N =     0b0001
    EMPTY = 0b0000
    BLOCK = 0b1111        

# @dataclass
# class RoomSchema:
#     hex: str

#     def __post_init__(self):
#         self.west, self.south, self.east, self.north = \
#             [x == '1' for x in bin(int(self.hex, 16) + 16)[3:]]
#         self.walls = [self.north, self.west, self.east, self.south]
#         self.__repr = {'north': '+--+', 'west': '| ', 'east': ' |', 'south': '+--+'}
        
# # neighbours: list['Room'] = field(repr=False, default_factory=list)

#     def __repr__(self) -> str:
#         result = ''
#         result += (self.__repr['north'] if self.walls[0] else '    ') + '\n'
#         result += (self.__repr['west'] if self.walls[1] else '  ')
#         result += (self.__repr['east'] if self.walls[2] else '  ') + '\n'
#         result += (self.__repr['south'] if self.walls[3] else '    ') + '\n'
#         return result

# TODO think if we even need low level here? maybe just maze is ok?
@dataclass(repr=False)
class Grid(list):
    width: int
    height: int

    def __init__(self, width: int, height: int, default: Any):
        self.width = width
        self.height = height
        super().__init__([[default for x in range(self.width)] 
                          for y in range(self.height)])
    
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
