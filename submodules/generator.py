from pydantic import BaseModel

from submodules.abstract import Vector
from submodules.data import Maze, Room, RoomData
from submodules.enums import Move, Wall


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

    def generate(self) -> Maze[RoomData]:
        """Generates maze.
        """

    # @property
    # def solution(self) -> list[]