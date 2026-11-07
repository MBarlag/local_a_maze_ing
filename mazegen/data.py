"""Specific classes for Maze, built on top of the abstract classes.

Defines data stored in each room of the maze, the Room Class with
wall-manipulation methods, and the Maze grid that holds entry and exit
coordinates.
"""

from functools import cached_property
from random import shuffle

from mazegen.abstract import Cell, Grid, Vector
from mazegen.enums import Step, Ways


class Room(Cell[None]):
    """Room of maze, stores info related for maze.

    Supports relative access of other rooms via self + offset.
    Or via self[offset], including self[step] or self[dx, dy].
    Square brackets mean the access can raise IndexError if not careful.
    self + offset will return None if outside of bounds.

    Attributes:
        visited: If room was visited or not.
        blocked: If the room walls cant be modified.
        walls: Configuration of existing walls directions.
        path_hint: A direction to take, to end up at maze exit.
    """

    visited: bool = False
    blocked: bool = False
    walls: Ways = Ways.ALL
    path_hint: Ways = Ways.NONE

    @property
    def deadend(self) -> bool:
        """Whether this room has 3 walls."""
        return self.walls.count == 3

    @cached_property
    def map(self) -> "dict[Room, Ways]":
        """Map of neighbours directions."""
        PRIMITIVE_MOVES = [
            (Ways.N, Step.UP),
            (Ways.S, Step.DOWN),
            (Ways.W, Step.LEFT),
            (Ways.E, Step.RIGHT),
        ]
        shuffle(PRIMITIVE_MOVES)
        neighbours = {}
        for direction, step in PRIMITIVE_MOVES:
            neighbour = self + step
            if neighbour is None:
                continue
            neighbours[neighbour] = direction
        return neighbours

    @cached_property
    def neighbours(self) -> "list[Room]":
        """List of neighbouring rooms."""
        return [n for n in self.map]

    @property
    def connections(self) -> "list[Room]":
        """Connected neighbours."""
        result = []
        for neighbour in self.neighbours:
            if neighbour.blocked:
                continue
            wall_between = self.map[neighbour]
            if wall_between not in self.walls:
                result.append(neighbour)
        return result

    @property
    def isolates(self) -> "list[Room]":
        """Not connected neighbours."""
        result = []
        for neighbour in self.neighbours:
            if neighbour.blocked:
                continue
            wall_between = self.map[neighbour]
            if wall_between in self.walls:
                result.append(neighbour)
        return result

    @property
    def valid(self) -> bool:
        """Whether the room's walls are coherent with its neighbours."""
        if self.walls == self.hugging_walls:
            return True
        return False

    def connect_with(self, neighbour: "Room") -> Ways:
        """Break wall between current Room and not blocked neighbour."""
        if self.blocked or neighbour.blocked:
            raise MazeError(
                "Trying to create a connection with a blocked room."
            )
        obstacle = self.map[neighbour]
        if obstacle in self.walls:
            self.walls -= obstacle
        if obstacle.opposite in neighbour.walls:
            neighbour.walls -= obstacle.opposite
        return obstacle

    def way_towards(self, neighbour: "Room") -> Ways:
        """Get direction towards the neighbour."""
        return self.map[neighbour]

    @property
    def hugging_walls(self) -> Ways:
        """Walls this room should have to be coherent with its neighbours."""
        hugging_walls = Ways.ALL
        for neighbour, wall in self.map.items():
            if wall.opposite not in neighbour.walls:
                hugging_walls -= wall
        return hugging_walls


class MazeError(Exception):
    """An exception happening during basic construction of maze."""


class Maze(Grid[None, Room]):
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
        super().__init__(width, height, default=None, cell_class=Room)
        self._set_entry(entry or Vector(0, 0))
        self._set_exit(exit or Vector(1, 0))
        if self.exit == self.entry:
            raise MazeError("Cant have entry == exit.")
        self.edges = 0

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
