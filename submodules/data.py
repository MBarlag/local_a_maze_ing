from dataclasses import dataclass
from enums import Wall, Move
from abstract import Grid, Cell


@dataclass
class RoomData:
    visited: bool
    walls: Wall


class Room(Cell[RoomData]):
    @property.getter
    def surrounded(self) -> list[Wall]:
        surrounded = [Wall.W, Wall.E, Wall.N, Wall.S]
        for wall in list(surrounded):
            neighbour = self + wall.direction
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                surrounded.remove(wall)
        return surrounded

    @property.getter
    def valid(self) -> bool:
        return self.walls == self.surrounded

    def break_wall(self, to_break: Wall) -> None:
        if to_break in self.walls:
            self.walls -= to_break
            neighbour = self + to_break.direction
            if neighbour is None:
                raise ValueError("Can't break borders of the maze")
            neighbour.walls -= to_break.opposite
        else:
            raise ValueError("Walls requested don't exist")


class Maze(Grid[RoomData]):
    def __init__(self, width: int, height: int, 
                 default: RoomData = RoomData(visited=False, walls=Wall.BLOCK)):
        super().__init__(width, height, default)
