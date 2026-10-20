from random import randint

from pydantic import BaseModel

from submodules.abstract import Grid, Vector
from submodules.data import Maze, Room, RoomData
from submodules.enums import Move

PATTERN_STRING = """
1000111
1000001
1110111
0010100
0010111
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

    # _draft_maze: Maze[RoomData] - maze that is in the making, doesnt need to be valid and should not be used by the user, is for internal working of the class

    # TODO create constructor that doesnt interfere with the BaseModel underlying logic (lookup how to do it)
    # TODO set self._last_maze to be None here

    def _refresh_seed(self) -> None:
        MIN_INT = -(2**31)
        MAX_INT = 2**31 - 1
        self.seed = randint(MIN_INT, MAX_INT)

    def generate(self, new_seed: bool = False) -> Maze:
        """Generates maze.

        Args:
            new_seed (bool, optional): Randomly pick new seed before generating maze. Defaults to False.

        Returns:
            Maze[RoomData]: Maze data structure.
        """
        if new_seed == True:
            self._refresh_seed()
        self._draft_maze = Maze(self.width, self.height, self.entry, self.exit)
        self._add_pattern()
        self._build_maze()
        if self._draft_maze.valid == False:
            raise Exception("Error during generation of Maze")
        self._last_maze = self._draft_maze
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

        To be able to avoid destructing walls of the pattern when generating maze. Should be called only after the self._draft_maze has been initialized.
        """
        # width for 42 pattern: 7 cells
        # height for 42 pattern: 5 cells
        pattern = Grid(7, 5, False)

        for y, line in enumerate(PATTERN_STRING.split("\n")):
            for x, character in enumerate(line):
                # 1 represents True, 0 represents False in the PATTERN_STRING
                pattern[y, x].value = character == "1"

        left_top = Vector(0, 0)
        left_top.y = (self.height - pattern.height) // 2
        left_top.x = (self.width - pattern.width) // 2

        left_top_room = self._draft_maze[left_top]
        # setting rooms that are corresponding to the pattern to blocked = True

        for cell in pattern:
            room = left_top_room + cell.as_vector
            if room:
                room.blocked = cell._value

    def valid_neighbour(self, neighbour: Room) -> bool:
        if (neighbour != None and neighbour.visited != True
                and neighbour.blocked != True):
            return False
        return True

    def bfs(self) -> None:
        queue: list[Room] = []
        entry = self._draft_maze[self.entry]
        queue.append(entry)
        while queue:
            popped = queue.pop()
            popped.visited = True
            neighbours = [popped.visit(*direction) for direction in list(Move)]
            neighbours = [x for x in neighbours if x != None]
            queue = list(neighbours)

    @property
    def last_maze(self) -> Maze[RoomData] | None:
        """Property that stores the Maze from last generate() call."""
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
