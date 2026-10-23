"""[TODO:description].

[TODO:description]
"""

from dataclasses import dataclass

from typing_extensions import Self

from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Move, Walls


@dataclass
class RoomData:
    visited: bool = False
    walls: Walls = Walls.BLOCK
    blocked: bool = False


class Room(Cell[RoomData]):
    @property
    def neighbours(self) -> list[Self]:
        """List of neighbouring rooms."""
        MAIN_DIRECTIONS = list(Move)[:4]
        neighbours: list[Self] = []
        for direction in MAIN_DIRECTIONS:
            neighbour = self + direction
            if neighbour is None:
                continue
            neighbours.append(neighbour)
        return neighbours

    @property
    def hugging_walls(self) -> Walls:
        surrounded = Walls.BLOCK
        for wall in Walls.BLOCK:
            neighbour = self + wall.direction
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                surrounded -= wall
        return surrounded

    @property
    def valid(self) -> bool:
        if self.walls == self.hugging_walls:
            return True
        return False

    # @property
    # def breakable_walls(self) -> Walls:
    #     breakable = Walls.BLOCK
    #     for wall in breakable:
    #         pass

    def break_wall(self, to_break: Walls) -> None:
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
        width: int,
        height: int,
        entry: Vector[int] | None = None,
        exit: Vector[int] | None = None,
    ):
        super().__init__(width, height, default=RoomData(), cell_class=Room)
        self._set_entry(entry or Vector(0, 0))
        self._set_exit(exit or Vector(0, 0))

    @property
    def valid(self) -> bool:
        return super().valid and self.entry != self.exit

    @property
    def room(self) -> Room:
        return self.cell

    @property
    def entry(self) -> Vector[int]:
        return self._entry

    def _set_entry(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError(
                f"Coordinates are not reachable. \
                {coord=}, {self.width=}, {self.height=}"
            )
        self._entry = coord

    @property
    def exit(self) -> Vector[int]:
        return self._exit

    def _set_exit(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError(
                f"Coordinates are not reachable. \
                {coord=}, {self.width=}, {self.height=}"
            )
        self._exit = coord
