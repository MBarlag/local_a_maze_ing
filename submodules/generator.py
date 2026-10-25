from random import randint, shuffle
from typing import Any

from pydantic import BaseModel, PrivateAttr

from submodules.abstract import Grid
from submodules.data import Maze, Room
from submodules.enums import Walls, Move
from submodules.safe_types import Bool, FileName, IntVector, PositiveInt


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
        self.dfs()

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

    def legal_neighbour(self, neighbour: Room) -> bool:
        """Legal neighbour for dfs maze generation."""
        if neighbour.blocked is False and neighbour.visited is False:
            return True
        return False

    # def bfs(self) -> list[Move]:
    #     maze = self._draft_maze
    #     start = maze[self.exit]

    #     # BFS first explores neighbours, before moving a level deeper.
    #     # Maintain a queue of nodes we have to visit next.

    #     queue: list[Room] = [start]
    #     counter = 0
    #     while counter < len(queue):
    #         current = queue[counter]
    #         counter += 1
    #         connections: list[Move] = []

    #         if not (current.Walls & Walls.N):
    #             connections.append(Move.UP)
    #         if not (current.Walls & Walls.E):
    #             connections.append(Move.RIGHT)
    #         if not (current.Walls & Walls.W):
    #             connections.append(Move.LEFT)
    #         if not (current.Walls & Walls.S):
    #             connections.append(Move.DOWN)

    #         for move in connections:

    #             # Convert room to neighbours and

    def bfs_find_path(self) -> None:
        """Finds shortest path through in an imperfect maze.

        Raises:
            ValueError: When there is no possible path between entry and exit.

        Returns:
            list[tuple[Room, Room]]: _description_
        """
        maze = self._draft_maze
        for room in maze:
            room.visited = False
            room.to_exit = Move.NOWHERE

        start = maze[self.exit]
        queue: list[tuple[Room, Room]] = [(start, start)]
        while queue:
            root, room = queue.pop(0)
            if room.visited:
                continue
            if root.as_vector != room.as_vector:
                direction = Move.v(root.as_vector - room.as_vector)
                room.to_exit = direction
            room.visited = True
            if room.as_vector == self.entry:
                break

            neighbours = []
            for wall in (Walls.N, Walls.E, Walls.S, Walls.W):
                if wall not in room.walls:
                    neighbour = room + wall.direction
                    if neighbour:
                        neighbours.append(neighbour)
            shuffle(neighbours)
            legal = filter(self.legal_neighbour, neighbours)
            queue.extend([(room, neighbour) for neighbour in legal])

        path: list[Walls] = []
        cell: Room | None = maze[self.entry]
        while cell and cell.as_vector != self.exit:
            if cell.to_exit == Move.NOWHERE:
                raise ValueError("Can't reach entry from exit")
            path.append(cell.choose_wall(cell.to_exit))                        
            cell += cell.to_exit
        self._path = path
        self.last_maze = maze

    def dfs(self) -> None:
        """Depth first search to create a perfect maze."""
        maze = self._draft_maze
        exit = maze[self.exit]

        # where we came from   # where we ended up

        # [(OriginalRoom, Room2), OriginalRoom, Room3, Room4]
        queue: list[tuple[Room, Room]] = [(exit, exit)]
        while queue:
            root, room = queue.pop()
            if room.visited is True:
                continue
            if root.as_vector != room.as_vector:
                direction = room.connect_with(root)
                room.to_exit = direction
                # room.connections.append(root)
            room.visited = True
            neighbours = list(room.neighbours)
            shuffle(neighbours)
            legal = filter(self.legal_neighbour, neighbours)
            queue.extend([(room, neighbour) for neighbour in legal])
            # print(queue)
            # print(maze)
        path: list[Walls] = []
        room = maze[self.entry]
        while room and room.as_vector != self.exit:
            if room:
                path.append(room.choose_wall(room.to_exit))
            new_room = room + room.to_exit
            if new_room:
                room = new_room
        self._path = path
        self.last_maze = maze

    def output(self) -> None:
        """Write generated maze to a file."""
        if not self.last_maze:
            raise Exception("No valid maze to output to file.")
        if not self._path:
            raise Exception("No path has been generated. Aborting output.")
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
