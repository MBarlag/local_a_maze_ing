from collections.abc import Callable
from random import randint, shuffle
from typing import Any

from pydantic import BaseModel, PrivateAttr

from submodules.abstract import Grid
from submodules.data import Maze, Room
from submodules.enums import Move, Walls
from submodules.safe_types import Bool, FileName, IntVector, PositiveInt


class MazeGenException(Exception):
    """An exception occuring during MazeGeneration."""


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
    _path: list[Walls] | None = PrivateAttr(None)

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
        """Initialize MazeGnerator inner attributes after its been created."""
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
        return self.last_maze

    def _build_maze(self) -> None:
        """Break walls of Maze keeping it valid to the constraints."""
        # here we have to constantly check with maze.valid
        # and if it became not valid, then we know we did something wrong
        # and we revert the changes back and try something else

        # trying something else means: we need to somehow know
        # our options, to choose from -> aka list that we iterate over

        # feel like drawing, goingto excalidraw
        self._last_maze = None
        maze = self._draft_maze
        exit = maze[self.exit]
        self._search(exit, self._connect_perfect, depth_first=True)
        if not self.perfect:
            self._reset_search_data()
            self._remove_deadends()
            self._reset_search_data()
            self._search(exit, self._find_path, depth_first=False)
            if not self._validate_packman():
                raise MazeGenException("Generated Maze is not Packman ready.")
        if not self._draft_maze.valid:
            raise MazeGenException("Generated Maze is not valid.")
        self.last_maze = self._draft_maze
        self._path = self._extract_path()
        self._output()

    def _validate_packman(self) -> bool:
        return True

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

        x = (self.width - pattern.width) // 2
        y = (self.height - pattern.height) // 2

        left_top_room = maze[x, y]
        # setting rooms that are corresponding to the pattern to blocked = True
        for cell in pattern:
            room = left_top_room + cell.as_vector
            if room:
                room.blocked = cell.value == Walls.BLOCK

    def _remove_deadends(self) -> None:
        pass

    def _reset_search_data(self) -> None:
        maze = self._draft_maze
        for room in maze:
            room.visited = False
            room.to_exit = Move.NOWHERE

    def _find_path(
        self, previous: Room, current: Room
    ) -> list[tuple[Room, Room]] | None:
        """Finds shortest path through in an imperfect maze.

        Raises:
            ValueError: When there is no possible path between entry and exit.

        Returns:
            list[tuple[Room, Room]]: _description_
        """
        if current.visited is True or current.blocked is True:
            return []
        if previous.as_vector != current.as_vector:
            direction = Move.v(previous.as_vector - current.as_vector)
            current.to_exit = direction
        current.visited = True
        if current.as_vector == self.entry:
            return None

        neighbours = []
        for wall in (Walls.N, Walls.E, Walls.S, Walls.W):
            if wall not in current.walls:
                neighbour = current + wall.direction
                if neighbour:
                    neighbours.append(neighbour)
        shuffle(neighbours)
        next_steps = [(current, neighbour) for neighbour in neighbours]
        return next_steps

    def _connect_perfect(
        self, previous: Room, current: Room
    ) -> list[tuple[Room, Room]] | None:
        """Connect rooms (perfect), return [(current, legal_neighbour), ..].

        Args:
            previous: Previous room from dfs search.
            current: Current room from dfs search.

        Returns:
            A list of tuples in a format of (from, to).
            'to' is populated by current room neighbours,
            that fall under criteria that define perfect maze
            generation: has not been visited and the subject criteria:
            is not part of the 42 pattern.
        """
        if current.visited is True or current.blocked is True:
            return []
        if previous.as_vector != current.as_vector:
            direction = current.connect_with(previous)
            current.to_exit = direction
            # room.connections.append(root)
        current.visited = True
        neighbours = list(current.neighbours)
        # TODO: create one access point for
        # lowering chance of missing one of the
        # functions and not adding reproducability there.
        # TODO: add seed reproducability here.
        shuffle(neighbours)
        legal = [(current, next_room) for next_room in neighbours]
        return legal

    def _search(
        self,
        start: Room,
        process_step: Callable[[Room, Room], list[tuple[Room, Room]] | None],
        depth_first: bool = True,
    ) -> None:
        """Search a maze and apply processing function each step.

        Adds new options that processing function returned to the queue.
        If process_step returned None => aborts the search.
        Otherwise aborts when the queue is empty.

        Args:
            start: [TODO:description]
            process_step: [TODO:description]
            depth_first: [TODO:description]
        """
        queue: list[tuple[Room, Room]] = [(start, start)]
        direction = -1 if depth_first else 0
        while queue:
            root, room = queue.pop(direction)
            new_options = process_step(root, room)
            if new_options is None:
                break
            queue.extend(new_options)

    def _extract_path(self) -> list[Walls]:
        maze = self.last_maze
        if not maze:
            raise MazeGenException("Valid Maze has not been generated.")
        path: list[Walls] = []
        room = maze[self.entry]
        while room and room.as_vector != self.exit:
            if room:
                path.append(room.choose_wall(room.to_exit))
            new_room = room + room.to_exit
            if new_room:
                room = new_room
        return path

    def _output(self) -> None:
        """Write generated maze to a file."""
        if not self.last_maze:
            raise MazeGenException("No valid maze to output to file.")
        if not self._path:
            raise MazeGenException(
                "No path has been generated. Aborting output."
            )
        maze = self.last_maze
        with open(self.output_file, "w", encoding="utf-8") as f:
            for y in range(maze.height):
                line = (
                    "".join(
                        hex(room.value.walls.value)[2:] for room in maze.row(y)
                    )
                    + "\n"
                )
                f.write(line)
            entry = str(self.entry).strip("()")
            exit = str(self.exit).strip("()")
            f.write(f"\n{entry}\n{exit}\n")
            f.write("".join(str(x) for x in self._path) + "\n")

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
