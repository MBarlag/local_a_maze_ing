import random
from collections import deque
from collections.abc import Callable, Iterable
from dataclasses import KW_ONLY, dataclass, field
from random import choice, randint

from submodules.abstract import Grid, Vector
from submodules.config import MazeConfig
from submodules.data import Maze, Room
from submodules.enums import Ways

P42_WIDTH = 7
P42_HEIGHT = 5

# MIN_WIDTH = 2
# MIN_HEIGHT = 2

P42_MIN_WIDTH = 9
P42_MIN_HEIGHT = 6


class MazeGenError(Exception):
    """An exception occuring during MazeGeneration."""


@dataclass
class MazeGenerator:
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

    # model_config = ConfigDict(arbitrary_types_allowed=True)
    _: KW_ONLY
    width: int
    height: int
    entry: Vector[int]
    exit: Vector[int]
    output_file: str
    perfect: bool
    seed: int | None = None
    _last_maze: Maze | None = field(init=False, repr=False, default=None)
    _path: list[Ways] | None = field(init=False, repr=False, default=None)
    _edges: int = field(init=False, repr=False, default=0)
    _rooms: int = field(init=False, repr=False, default=0)

    def __post_init__(
        self,
    ) -> None:
        """Initialize MazeGnerator inner attributes after its been created."""
        # self.width = config.width
        # self.height = config.height
        # self.entry = config.entry
        # self.exit = config.exit
        # self.perfect = config.perfect
        # self.output_file = config.output_file
        # self.seed = config.seed
        unchecked = vars(self)
        maze_config = MazeConfig(**unchecked)
        checked = vars(maze_config)
        for name, value in checked.items():
            setattr(self, name, value)
        if not self.perfect and (self.width == 1 or self.height == 1):
            raise MazeGenError(
                "Pacman cannot have width or height equal to 1."
            )
        # if not self.perfect and (self.width == 2 and self.height == 2):
        #     raise MazeGenError("bleh")
        self._draft_maze = Maze(self.width, self.height, self.entry, self.exit)
        origin = self._draft_maze.room
        if origin + self.entry is None or origin + self.exit is None:
            raise MazeGenError("Entry and/or exit are out of bounds.")
        if self.seed is None:
            self.seed = self.set_seed()

    def set_seed(self, value: int | None = None) -> int:
        """Regenerate the seed."""
        MIN = 0
        MAX = 2**31 - 1

        if value is not None:
            random.seed(value)
            self.seed = value
            return value

        random.seed(0)
        new_seed = randint(MIN, MAX)
        random.seed(new_seed)
        self.seed = new_seed
        return self.seed

    def generate(self, new_seed: int | None = None) -> Maze:
        """Generates maze.

        Args:
            new_seed (bool, optional): Randomly pick new seed
                  before generating maze. Defaults to False.

        Returns:
            Maze: Maze data structure.
        """
        if new_seed is not None:
            self.set_seed(new_seed)
        self._draft_maze = Maze(self.width, self.height, self.entry, self.exit)
        maze = self._draft_maze
        entry = maze[self.entry]
        exit = maze[self.exit]
        self._add_pattern()
        if entry.blocked or exit.blocked:
            raise MazeGenError("Entry and exit cant be in pattern.")
        MAX_ATTEMPTS = 20
        for _ in range(MAX_ATTEMPTS):
            try:
                self._build_maze()
                break
            except Exception:
                pass
        # if the loop didnt have a break
        else:
            print(maze.view(lambda x: str(x.walls)))
            raise MazeGenError(
                "[ERROR] Failed not create maze for the current configuration."
            )
        result = self.last_maze
        return result

    def is_pacman(self) -> bool:
        """Checks if the maze has more than one loop."""
        return (self._edges - (self._rooms) + 1) >= 2

    def _build_maze(self) -> None:
        """Break walls of Maze keeping it valid to the constraints."""
        self._edges = 0
        self._rest_walls()
        maze = self._draft_maze
        exit = maze[self.exit]
        self._reset_states()
        self._walk(exit, on_each_visit=self._connect, depth_first=True)
        if not self.perfect:
            self._remove_deadends()
            self._reset_states()
            self._walk(exit, on_each_visit=self._find_path, depth_first=False)
            if not self.is_pacman():
                raise MazeGenError(
                    "Not enough loops for pacman. Need at least 2."
                )
        if not self._is_connected():
            raise MazeGenError("Generated Maze is not fully connected.")
        if not self._draft_maze.valid:
            raise MazeGenError("Generated Maze is not valid.")
        self.last_maze = self._draft_maze
        self._path = self._extract_path()
        self._output()

    def _add_pattern(self) -> None:
        """Set the rooms that are part of the pattern to blocked true.

        To be able to avoid destructing walls
        of the pattern when generating maze.
        Should be called only after the self._draft_maze has been called.
        """
        maze = self._draft_maze
        if self.width < P42_MIN_WIDTH or self.height < P42_MIN_HEIGHT:
            print("Pattern doesn't fit Mazes width or height, skipping it.")
            self._rooms = self.height * self.width
            return
        self._rooms = self.height * self.width - 18
        pattern = Grid(
            P42_WIDTH,
            P42_HEIGHT,
            from_file="42.txt",
            on_each_char=lambda c: Ways(int(c, 16)),
        )
        x = (self.width - pattern.width) // 2
        y = (self.height - pattern.height) // 2
        if self.width % 2 == 0:
            x += 1
        if self.height % 2 == 0:
            y += 1

        left_top_room = maze[x, y]
        # setting rooms that are corresponding to the pattern to blocked = True
        for cell in pattern:
            room = left_top_room + cell.as_vector
            if room:
                room.blocked = cell.value == Ways.ALL

    # expected to be called only after fresh _find_path execution
    def _is_connected(self) -> bool:
        maze = self._draft_maze
        exit = maze[self.exit]
        entry = maze[self.entry]
        if exit.walls == Ways.ALL or entry.walls == Ways.ALL:
            return False
        for room in maze:
            to_next = room.path_hint
            if room is exit:
                continue
            if to_next is Ways.NONE and not room.blocked:
                return False
        return True

    def _rest_walls(self) -> None:
        maze = self._draft_maze
        for room in maze:
            room.walls = Ways.ALL

    def _reset_states(self) -> None:
        maze = self._draft_maze
        for room in maze:
            room.visited = False
            room.path_hint = Ways.NONE

    def _find_path(
        self, old_room: Room, current_room: Room
    ) -> list[Room] | None:
        """Finds shortest path in a maze.

        Raises:
            # TODO: make this possible
            ValueError: When there is no possible path between entry and exit.

        Returns:
            list[Room] | None: Empty list if room
            has been visited or is blocked, otherwise a list with rooms
            that can be visited.
        """
        if current_room.visited or current_room.blocked:
            return []
        direction = old_room.way_towards(current_room)
        if direction in old_room.walls:
            return []
        current_room.path_hint = direction.opposite
        current_room.visited = True
        # could be aborted earlier, but we need
        # to use the data for maze connectivity checks.
        # if current.as_vector == self.entry:
        #     return None
        neighbours = current_room.neighbours
        return neighbours

    def _remove_deadends(self) -> None:
        maze = self._draft_maze
        for room in maze:
            if room.blocked or not room.deadend:
                continue
            if room.isolates == []:
                continue
            deadends = [r for r in room.isolates if r.deadend]
            selected = choice(deadends or room.isolates)
            room.connect_with(selected)
            self._edges += 1
        for room in maze:
            if self.is_pacman():
                break
            if room.blocked:
                continue
            if room.isolates == []:
                continue
            deadends = [r for r in room.isolates if r.deadend]
            selected = choice(deadends or room.isolates)
            room.connect_with(selected)
            self._edges += 1

    def _connect(self, previous: Room, current: Room) -> list[Room] | None:
        r"""Connect rooms and return \[legal_neighbour, ...].

        Skips room if room has been visited or
        the subject criteria:
        if room is part of the 42 pattern (blocked).

        Args:
            previous: Previous room from dfs search.
            current: Current room from dfs search.

        Returns:
            A list of tuples in a format of (from, to).
            'to' is populated by current room neighbours.
        """
        if current.visited or current.blocked:
            return []
        direction = previous.connect_with(current)
        self._edges += 1
        current.path_hint = direction.opposite
        current.visited = True
        neighbours = current.neighbours
        return neighbours

    def _walk(
        self,
        start_from: Room,
        on_each_visit: Callable[[Room, Room], Iterable[Room] | None],
        depth_first: bool = True,
    ) -> None:
        """Walk a maze and apply processing function each step.

        Adds new walking options that processing function
        returned to the queue.
        Processing function can return an empt list, which means
        no new options has been selected on the current steps.
        If on_each_visit function returned None => _walk completes.
        Otherwise _walk completes when the queue is empty.

        Args:
            start_from: [TODO:description]
            on_each_visit: [TODO:description]
            depth_first: [TODO:description]
        """
        start_from.visited = True
        queue: deque[tuple[Room, Room]] = deque(
            [(start_from, neighbour) for neighbour in start_from.neighbours]
        )
        POP_NEWEST = queue.pop
        POP_OLDEST = queue.popleft
        peek_new_rooms = on_each_visit
        get_next_idea = POP_NEWEST if depth_first else POP_OLDEST
        while queue:
            from_room, to_room = get_next_idea()
            new_rooms = peek_new_rooms(from_room, to_room)
            if new_rooms is None:
                break
            new_ideas = [(to_room, next_room) for next_room in new_rooms]
            queue.extend(new_ideas)

    def _extract_path(self) -> list[Ways]:
        """Extract a path from maze. Convert directions Walls repr."""
        maze = self.last_maze
        room: Room | None = maze[self.entry]
        path: list[Ways] = []
        while room and room.as_vector != self.exit:
            if room.path_hint is Ways.NONE:
                raise MazeGenError("Invalid path, encountered Ways.NONE.")
            path.append(room.path_hint)
            room = room + room.path_hint.as_step
        return path

    def _output(self) -> None:
        """Write generated maze to a file."""
        maze = self.last_maze
        with open(self.output_file, "w", encoding="utf-8") as f:
            for y in range(maze.height):
                line = "".join(room.walls.hex for room in maze.row(y)) + "\n"
                f.write(line)
            entry = str(self.entry).strip("()")
            exit = str(self.exit).strip("()")
            f.write(f"\n{entry}\n{exit}\n")
            f.write("".join(str(x) for x in self.path) + "\n")

    @property
    def path(self) -> list[Ways]:
        """The path property."""
        if self._path is None:
            raise MazeGenError("No path has been collected.")
        return self._path

    @path.setter
    def path(self, value: list[Ways]) -> None:
        self._path = value

    @property
    def last_maze(self) -> Maze:
        """Last generated maze."""
        if self._last_maze is None:
            raise MazeGenError(
                "Error accessing last maze, no maze has been generated."
            )
        return self._last_maze

    @last_maze.setter
    def last_maze(self, value: Maze) -> None:
        self._last_maze = value
