from dataclasses import dataclass

from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Wall


@dataclass
class RoomData:
    visited: bool = False
    walls: Wall = Wall.BLOCK
    blocked: bool = False


class Room(Cell[RoomData]):
    @property
    def surrounded(self) -> Wall:
        surrounded = Wall.BLOCK
        for wall in Wall.BLOCK:
            neighbour = self + wall.direction
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                surrounded -= wall
        return surrounded

    @property
    def valid(self) -> bool:
        if self.walls == sum(self.surrounded):
            return True
        return False

    def break_wall(self, to_break: Wall) -> None:
        if to_break in self.walls:
            self.walls -= to_break
            neighbour = self + to_break.direction
            if neighbour is None:
                raise ValueError("Can't break borders of the maze")
            neighbour.walls -= to_break.opposite
        else:
            raise ValueError("Walls requested don't exist")


class Maze(Grid[RoomData, Room]):
    def __init__(
        self,
        height: int,
        width: int,
        entry: Vector[int] = Vector(0, 0),
        exit: Vector[int] = Vector(0, 0),
    ):
        super().__init__(height, width, RoomData(), cell_class=Room)
        self._set_entry(entry)
        self._set_exit(exit)

    # TODO make a property .room, that basically wraps around .cell and returns so that semantically it makes more sense
    # TODO look into fixing the error that occurs when this property is added
    @property
    def room(self) -> Room:
        return self.cell

    @property
    def entry(self) -> Vector[int]:
        return self._entry

    def _set_entry(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError("Coordinates are not reachable")
        self._entry = coord

    @property
    def exit(self) -> Vector[int]:
        return self._exit

    def _set_exit(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError("Coordinates are not reachable")
        self._exit = coord
