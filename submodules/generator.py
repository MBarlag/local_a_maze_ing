from pydantic import BaseModel

from submodules.abstract import Vector
from submodules.data import Maze, Room, RoomData
from submodules.enums import Move, Wall

from functools import cache

class MazeGenerator(BaseModel):
    """Generates maze and stores all needed data for doing so.

    Attributes:
        width (int): Number of columns.
        height (int): Number of rows.
        entry (Vector[int]): Coordinates of entry point.
        exit (Vector[int]): Coordinates of exit point.
        output_file (str): Path to the hexadecimal file.
        perfect (bool): Enforce one unique path between any two points
        seed (int): Number that defines everything about the maze.
    """
    width: int
    height: int
    entry: Vector[int]
    exit: Vector[int]
    perfect: bool
    output_file: str
    seed: int

    # _maze: Maze[Room]
    @property
    def maze(self) -> Maze[RoomData]:
        """Generates maze.
        """

    # @property
    # def solution(self) -> list[]

    def shortest_path(self) -> list[Move]:
        """Finds a path through the given maze.

        Args:
            maze: The maze in which to find the path.

        Returns:
            list[Move]: _description_
        """

    def hex_output(self) -> list[list[int]]:
        """Create a file that stores the maze in hexadecimal.

        Returns:
            list[list[int]]: Holds maze, entry/exit and path.
        """
    