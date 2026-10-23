from random import randint
from typing import Any

from pydantic import BaseModel, PrivateAttr

from submodules.abstract import Grid
from submodules.data import Maze, Room
from submodules.enums import Walls
from submodules.safe_types import Bool, FileName, IntVector, PositiveInt

PATTERN_STRING = """
f000fff
f00000f
fff0fff
00f0f00
00f0fff
"""


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

    width: PositiveInt
    height: PositiveInt
    entry: IntVector
    exit: IntVector
    perfect: Bool
    output_file: FileName
    seed: PositiveInt
    _last_maze: Maze | None = PrivateAttr(None)
    _draft_maze: Maze = PrivateAttr()

    @property
    def last_maze(self) -> Maze | None:
        """Last generated maze.

        Returns:
            Maze or None if no maze has been generated.
        """
        return self._last_maze

    @last_maze.setter
    def last_maze(self, value: Maze) -> None:
        self._last_maze = value

    def model_post_init(self, context: Any) -> None:
        self._draft_maze = Maze(self.width, self.height, self.entry, self.exit)

    def _refresh_seed(self) -> None:
        """Regenerate the seed."""
        MIN_INT = -(2**31)
        MAX_INT = 2**31 - 1
        self.seed = randint(MIN_INT, MAX_INT)

    def generate(self, new_seed: bool = False) -> Maze | None:
        """Generates maze.

        Args:
            new_seed (bool, optional): Randomly pick new seed
                  before generating maze. Defaults to False.

        Returns:
            Maze: Maze data structure.
        """
        if new_seed is True:
            self._refresh_seed()
        self._draft_maze: Maze = Maze(
            self.width, self.height, self.entry, self.exit
        )
        self._add_pattern()
        self._build_maze()
        if self._draft_maze.valid is False:
            raise Exception("Error during generation of Maze")
        self.last_maze: Maze = self._draft_maze
        return self.last_maze

    def _build_maze(self) -> None:
        """Break walls of Maze keeping it valid to the constraints."""
        # here we have to constantly check with maze.valid
        # and if it became not valid, then we know we did something wrong
        # and we revert the changes back and try something else

        # trying something else means: we need to somehow know
        # our options, to choose from -> aka list that we iterate over

        # feel like drawing, goingto excalidraw

    def _add_pattern(self) -> None:
        """Set the rooms that are part of the pattern to blocked true.

        To be able to avoid destructing walls
        of the pattern when generating maze.
        Should be called only after the self._draft_maze has been called.
        """
        maze = self._draft_maze
        # width for 42 pattern: 7 cells
        # height for 42 pattern: 5 cells
        pattern = Grid(
            7, 5, from_file="42.txt", map_char=lambda c: Walls(int(c, 16))
        )
        
        another_pattern = Grid(7, 5, from_file="42.txt", map_char=lambda c: c == 'f')

        path = "EWNSNENWNNNEWN"
        transformed_path = [x for x in map(lambda c: 1, path)]

        x = (self.width - pattern.width) // 2
        y = (self.height - pattern.height) // 2

        left_top_room = maze[x, y]
        # setting rooms that are corresponding to the pattern to blocked = True
        for cell in pattern:
            room = left_top_room + cell.as_vector
            if room:
                room.blocked = cell.value == Walls.BLOCK

    def legal_moves(self, neightbour: Room) -> bool:
        return not (neightbour.blocked is True or neightbour.visited is True)

    def bfs(self) -> None:
        maze = self._draft_maze
        entry = maze[self.entry]
        queue: list[Room] = [entry]
        while queue:
            popped = queue.pop()
            popped.visited = True
            filtered = filter(self.legal_moves, popped.neighbours)
            queue.extend(filtered)

    # def shortest_path(self) -> list[Move]:
    #     """Finds a path through the given maze.
    #
    #     Args:
    #         maze: The maze in which to find the path.
    #
    #     Returns:
    #         list[Move]: List of moves that can be performed
    #         to reach the exit from the entry.
    #     """
    #
    # def hex_output(self) -> list[list[int]]:
    #     """Create a file that stores the maze in hexadecimal.
    #
    #     Returns:
    #         list[list[int]]: Holds maze, entry/exit and path.
    #     """
