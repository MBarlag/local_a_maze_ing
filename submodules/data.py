"""Specific classes for Maze, built on top of the abstract classes.

Defines data stored in each room of the maze, the Room Class with
wall-manipulation methods, and the Maze grid that holds entry and exit
coordinates.
"""

from dataclasses import dataclass

from typing_extensions import Self

from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Move, Walls


@dataclass
class RoomData:
    """Data stored inside each Room of the Maze.

    Attributes:
        visited: If room was visited during generation or finding path.
        walls: Combination of walls room currently has.
        blocked: If room is in the "42" pattern and may not be changed.
    """

    visited: bool = False
    walls: Walls = Walls.BLOCK
    blocked: bool = False
    to_exit: Move = Move.NOWHERE


class Room(Cell[RoomData]):
    """Cell of the Maze that stores RoomData and manages its walls.

    Attributes of RoomData (visited, walls, blocked) can be accessed
    directly on the Room, example: room.walls instead of room.value.walls.
    """

    @property
    def to_exit(self) -> Move:
        """A move needed to take, to get to the exit."""
        return self.value.to_exit

    @to_exit.setter
    def to_exit(self, value: Move) -> None:
        self.value.to_exit = value

    @property
    def neighbours(self) -> list[Self]:
        """List of neighbouring rooms.

        The four main directions (left, down, right, up) are checked.
        Positions out of bounds of the maze are skipped.

        Returns:
            Rooms directly next to this room.
        """
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
        """Walls this room should have to be coherent with its neighbours.

        Returns:
            Combination of walls that agree with the surrounding rooms.
        """
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
        """Whether the room's walls are coherent with its neighbours.

        Returns:
            bool: True if the room's walls match its hugging walls,
            False otherwise.
        """
        if self.walls == self.hugging_walls:
            return True
        return False

    def connect_with(self, neighbour: Self) -> Move:
        """Connect current Room with the neighbouring room.

        Args:
            neighbour (Self): # TODO add docsting.

        Raises:
            ValueError: If the wall is on the border of the maze,
            or if the room doesn't have the requested wall.
        """
        vector = neighbour.as_vector - self.as_vector
        direction = Move.v(vector)
        wall_to_break = self.choose_wall(direction)

        if wall_to_break in self.walls:
            self.walls -= wall_to_break
            neighbour.walls -= wall_to_break.opposite
        return direction

    def choose_wall(self, direction: Move) -> Walls:
        if direction == Move.LEFT:
            return Walls.W
        elif direction == Move.RIGHT:
            return Walls.E
        elif direction == Move.UP:
            return Walls.N
        elif direction == Move.DOWN:
            return Walls.S
        else:
            raise ValueError(
                "Argument isn't one of the primitive four directions"
            )


class Maze(Grid[RoomData, Room]):
    """Grid of Rooms including an entry and exit point.

    Access rooms through maze[x, y].
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
            width (int): Number of columns.
            height (int): Number of rows.
            entry: Coordinates of the entry point. Defaults to (0, 0).
            exit: Coordinates of the exit point. Defaults to (0, 0).
        """
        super().__init__(width, height, default=RoomData(), cell_class=Room)
        self._set_entry(entry or Vector(0, 0))
        self._set_exit(exit or Vector(0, 0))

    @property
    def valid(self) -> bool:
        """Returns whether the maze is valid."""
        return super().valid and self.entry != self.exit

    @property
    def room(self) -> Room:
        """Returns first Room of the Maze (0,0)."""
        return self.cell

    @property
    def entry(self) -> Vector[int]:
        """Returns coordinates of the entry point."""
        return self._entry

    def _set_entry(self, coord: Vector[int]) -> None:
        """Set entry point when it lies within the maze.

        Args:
            coord (Vector[int]): Coordinates of the entry point.

        Raises:
            ValueError: If coordinates are out of mazes bounds.
        """
        if self.cant_reach(*coord):
            raise ValueError(
                f"Coordinates are not reachable. \
                {coord=}, {self.width=}, {self.height=}"
            )
        self._entry = coord

    @property
    def exit(self) -> Vector[int]:
        """Returns coordinates of the exit point."""
        return self._exit

    def _set_exit(self, coord: Vector[int]) -> None:
        """Set exit point when it lies within the maze.

        Args:
            coord (Vector[int]): Coordinates of the exit point.

        Raises:
            ValueError: If coordinates are out of mazes bounds.
        """
        if self.cant_reach(*coord):
            raise ValueError(
                f"Coordinates are not reachable. \
                {coord=}, {self.width=}, {self.height=}"
            )
        self._exit = coord
