"""Specific classes for Maze, built on top of the abstract classes.

Defines data stored in each room of the maze, the Room Class with
wall-manipulation methods, and the Maze grid that holds entry and exit
coordinates.
"""

from dataclasses import dataclass
from functools import cached_property

from typing_extensions import Self

from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Step, Ways


@dataclass
class RoomData:
    """Data stored inside each Room of the Maze.

    Attributes:
        visited: If room was visited during generation or finding path.
        walls: Directions of walls the room currently has.
        blocked: If room is in the "42" pattern and may not be changed.
        path_hint: A direction one should take to end up at the exit.
    """

    visited: bool = False
    blocked: bool = False
    walls: Ways = Ways.ALL
    path_hint: Ways = Ways.NONE


class Room(Cell[RoomData]):
    """Has Roomdata, manages connections with other rooms.

    Supports relative acces of other rooms via self + offset.
    Or via self[offset], including self[step] or self[dx, dy].
    Square brackets mean the access can raise IndexError if not careful.
    self + offset will return None if outside of bounds.

    Attributes of RoomData (visited, walls, blocked) can be accessed
    directly on the Room, example: room.walls instead of room.value.walls.
    """

    @property
    def deadend(self) -> bool:
        """Whether this room has 3 walls."""
        return self.walls.count == 3

    @cached_property
    def neighbours(self) -> list[Self]:
        """List of neighbouring rooms."""
        PRIMITIVE_MOVES = list(Step)[:4]
        neighbours: list[Self] = []
        for direction in PRIMITIVE_MOVES:
            neighbour = self + direction
            if neighbour is None:
                continue
            neighbours.append(neighbour)
        return neighbours

    @property
    def connections(self) -> list[Self]:
        """Connected neighbours."""
        result = []
        for neighbour in self.neighbours:
            if neighbour.blocked:
                continue
            wall_between = self.way_towards(neighbour)
            if wall_between not in self.walls:
                result.append(neighbour)
        return result

    @property
    def isolates(self) -> list[Self]:
        """Not connected neighbours."""
        result = []
        for neighbour in self.neighbours:
            if neighbour.blocked:
                continue
            wall_between = self.way_towards(neighbour)
            if wall_between in self.walls:
                result.append(neighbour)
        return result

    @property
    def valid(self) -> bool:
        """Whether the room's walls are coherent with its neighbours."""
        if self.walls == self.hugging_walls:
            return True
        return False

    def connect_with(self, neighbour: Self) -> Ways:
        """Break wall between current Room and not blocked neighbour."""
        if self.blocked or neighbour.blocked:
            raise MazeError(
                "Trying to create a connection with a blocked room."
            )
        obstacle = self.way_towards(neighbour)
        if obstacle in self.walls:
            self.walls -= obstacle
        if obstacle.opposite in neighbour.walls:
            neighbour.walls -= obstacle.opposite
        return obstacle

    def way_towards(self, neighbour: Self) -> Ways:
        """Get direction towards the neighbour."""
        vector = neighbour.as_vector - self.as_vector
        step = Step.v(vector)
        return Ways.from_step(step)
        raise MazeError("Argument is not a neighbour.")

    @property
    def hugging_walls(self) -> Ways:
        """Walls this room should have to be coherent with its neighbours."""
        hugging_walls = Ways.ALL
        for wall in Ways.ALL:
            neighbour = self + wall.as_step
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                hugging_walls -= wall
        return hugging_walls

    @property
    def blocked(self) -> bool:
        """Whether the walls of the room can be removed."""
        return self.value.blocked

    @blocked.setter
    def blocked(self, value: bool) -> None:
        self.value.blocked = value

    @property
    def walls(self) -> Ways:
        """Walls of the room."""
        return self.value.walls

    @walls.setter
    def walls(self, value: Ways) -> None:
        self.value.walls = value

    @property
    def path_hint(self) -> Ways:
        """Direction hint, to get to the exit."""
        return self.value.path_hint

    @path_hint.setter
    def path_hint(self, value: Ways) -> None:
        self.value.path_hint = value


class MazeError(Exception):
    """An exception happening during basic construction of maze."""


class Maze(Grid[RoomData, Room]):
    """Grid of Rooms including an entry and exit point.

    Access rooms through maze[x, y]. Raises IndexError with wrong coords.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Vector[int] | None = None,
        exit: Vector[int] | None = None,
    ):
        """Create a Maze where every room has all its walls.

        Args:
            width: Number of columns.
            height: Number of rows.
            entry: Coordinates of the entry point. Defaults to (0, 0).
            exit: Coordinates of the exit point. Defaults to (0, 0).
        """
        super().__init__(width, height, default=RoomData(), cell_class=Room)
        self._set_entry(entry or Vector(0, 0))
        self._set_exit(exit or Vector(0, 0))

    @property
    def valid(self) -> bool:
        """Whether the maze is valid."""
        entry = self.room + self.entry
        exit = self.room + self.exit
        if entry is None:
            raise MazeError("Entry is out of bounds.")
        if exit is None:
            raise MazeError("Exit is out of bounds.")
        return super().valid and self.entry != self.exit

    @property
    def room(self) -> Room:
        """Returns first Room of the Maze (0,0)."""
        return self.cell

    @property
    def entry(self) -> Vector[int]:
        """Coordinates of the entry point."""
        return self._entry

    def _set_entry(self, coord: Vector[int]) -> None:
        """Set entry point when it lies within the maze."""
        if self.cant_reach(*coord):
            raise ValueError(
                f"Coordinates are not reachable. \
                {coord=}, {self.width=}, {self.height=}"
            )
        self._entry = coord

    @property
    def exit(self) -> Vector[int]:
        """Coordinates of the exit point."""
        return self._exit

    def _set_exit(self, coord: Vector[int]) -> None:
        """Set exit point when it lies within the maze."""
        if self.cant_reach(*coord):
            raise ValueError(
                f"Coordinates are not reachable. \
                {coord=}, {self.width=}, {self.height=}"
            )
        self._exit = coord
