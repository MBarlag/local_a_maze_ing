from random import randint

from pydantic import BaseModel

from submodules.abstract import Vector, Grid
from submodules.data import Maze, RoomData
from submodules.enums import Move


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

    # last_maze: Maze[RoomData] - gonna store last generated maze, 
    # its up to user
    # to call generate again if they have made any changes to the MazeGenerator # instance, and they can always access the result of last generation via 
    # this property


    # TODO create constructor that doesnt interfere with the BaseModel underlying logic (lookup how to do it)
    # TODO set self._last_maze to be None here

    def _refresh_seed(self) -> None:
        MIN_INT = -2 ** 31
        MAX_INT = 2 ** 31 - 1
        self.seed = randint(MIN_INT, MAX_INT)

    def generate(self, new_seed: bool = False) -> Maze[RoomData]:
        """Generates maze.

        Args:
            new_seed (bool, optional): Randomly pick new seed before generating maze. Defaults to False.

        Returns:
            Maze[RoomData]: Maze data structure.
        """
        if new_seed == True:
            self._refresh_seed()    

    def add_pattern(self) -> None:
        pattern = Grid(7, 5, False)

        with open("pattern.txt", "r") as file:
            for y, line in enumerate(file.readlines()):
                for x, character in enumerate(line):
                    pattern[y][x] = character
        
        # Set the rooms that are part of the pattern to locked: true.
        # To be able to avoid destructing walls of the pattern when generating maze.
        left_top_corner = y = self.height / 2 

        # Open the pattern.txt and 
        # Min width for pattern: 7 cells
        # Min height for pattern: 5 cells

    @property
    def last_maze(self) -> Maze[RoomData] | None:
        """Property that stores the Maze from last generate() call.

        Returns:
            Maze[RoomData] | None: Maze data structure, or None in case nothing was generated.
        """        
        return self._last_maze


    def shortest_path(self) -> list[Move]:
        """Finds a path through the given maze.

        Args:
            maze: The maze in which to find the path.

        Returns:
            list[Move]: List of moves that can be performed to reach the exit from the entry.
        """

    def hex_output(self) -> list[list[int]]:
        """Create a file that stores the maze in hexadecimal.

        Returns:
            list[list[int]]: Holds maze, entry/exit and path.
        """
    