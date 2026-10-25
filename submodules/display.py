from pydantic import BaseModel, Field

from submodules.abstract import Vector
from submodules.enums import Walls

ENTRY_FLAG = 1 << 4
EXIT_FLAG = 1 << 5
PATH_OFFSET = 6
PATH_N = 1 << PATH_OFFSET
PATH_E = PATH_N << 1
PATH_S = PATH_N << 2
PATH_W = PATH_N << 3
PATH = PATH_W + PATH_S + PATH_E + PATH_N

CLR = "63"
PATH_CLR = "\033[38;5;82m\033[48;5;82m"  # yellow 220
COLOR_1 = f"\033[38;5;{CLR}m\033[48;5;{CLR}m"
COLOR_2 = "\033[38;5;53m\033[48;5;53m"
RST = "\033[0m"


class MazePrinter(BaseModel):
    """Parses and displays hexadecimal file as readable maze in terminal.

    Attributes:
        width (int): Number of columns.
        height (int): Number of rows.
        entry (str): Coordinates of entry point.
        exit (str): Coordinates of exit point.
        input_file (str): Path to the hexadecimal file.
    """

    width: int
    height: int
    entry: str
    exit: str
    input_file: str = Field(alias="output_file")
    path_visible: bool = False
    wall_color: str = COLOR_1

    @staticmethod
    def _parse_coords(coord: str) -> tuple[int, int]:
        """Converts coordinate string into (x, y) tuple.

        Args:
            coord (str): The coordinate str, as read from config.txt.

        Returns:
            tuple[int, int]: The coordinates parsed to a tuple.
        """
        xy = coord.split(",")
        x = int(xy[0])
        y = int(xy[1])
        return x, y

    def _parse_hex(self) -> list[list[int]]:
        """Reads maze lines from hexadecimal file to a list of list[int].

        Returns:
            list[list[int]]: Holds maze cells and entry/exit points.
        """
        hex_maze: list[list[int]] = []
        with open(self.input_file, "r") as file_obj:
            for line in file_obj:
                line = line.strip()
                if not line:
                    break
                hex_maze.append([int(char, 16) for char in line])

        self._mark_point(ENTRY_FLAG, self.entry, hex_maze)
        self._mark_point(EXIT_FLAG, self.exit, hex_maze)
        if self.path_visible:
            self._mark_path(hex_maze)
        return hex_maze

    def _mark_point(
            self, flag: int, coord_str: str, hex_maze: list[list[int]]
            ) -> None:
        """Adds entry or exit point to hex_maze file.

        Args:
            flag (int): Orchestrates whether to mark entry or exit.
            coord_str (str): The coordinates for entry/exit.
            hex_maze (list[list[int]]): Holds maze cells and entry/exit points.
        """
        x, y = self._parse_coords(coord_str)
        hex_maze[y][x] |= flag

    def _display_row(self, hex_row: list[int]) -> None:
        """Prints North and West walls of maze row and closes with + and |.

        Args:
            hex_row (list[int]): One line of hexadecimal characters.
        """
        north = 1
        west = 8
        block = 15
        WCLR = self.wall_color
        for cell in hex_row:
            print(f"{WCLR}+{RST}", end="")
            if cell & north:
                print(f"{WCLR}---{RST}", end="")
            elif cell & PATH:
                print(f"{PATH_CLR}   {RST}", end="")
            else:
                print("   ", end="")
        print(f"{WCLR}+{RST}")

        for cell in hex_row:
            if cell & west:
                print(f"{WCLR}|{RST}", end="")
            elif cell & PATH:
                print(f"{PATH_CLR} {RST}", end="")
            else:
                print(" ", end="")

            if cell & ENTRY_FLAG:
                print(" A ", end="")
            elif cell & EXIT_FLAG:
                print(" B ", end="")
            elif cell & PATH:
                if cell & PATH_W:
                    print(f"{PATH_CLR} < {RST}", end="")
                elif cell & PATH_S:
                    print(f"{PATH_CLR} v {RST}", end="")
                elif cell & PATH_E:
                    print(f"{PATH_CLR} > {RST}", end="")
                elif cell & PATH_N:
                    print(f"{PATH_CLR} ^ {RST}", end="")
            elif (cell & block) == block:
                print("███", end="")
            else:
                print("   ", end="")
        print(f"{WCLR}|{RST}")

    def _display_bottom(self) -> None:
        """Prints the closing South walls of the maze."""
        WCLR = self.wall_color
        for _ in range(self.width):
            print(f"{WCLR}+---{RST}", end="")
        print(f"{WCLR}+{RST}")

    def _parse_path(self) -> str:
        """Reads the path line with moves from the hex_maze file.

        Returns:
            str: The moves of the path.
        """
        with open(self.input_file, "r") as file_obj:
            lines = [line.strip() for line in file_obj]

        return lines[-1]

    def _mark_path(self, hex_maze: list[list[int]]) -> None:
        """Reads path starting at entry and flags room on the path."""
        entry = Vector(*self._parse_coords(self.entry))
        position = entry
        path_str = self._parse_path()
        for step in path_str:
            #     if step not in ("N", "E", "S", "W"):
            #         raise ValueError("Invalid path character in input file.")
            if position == entry:
                position += Walls[step].direction
                continue
            x, y = position
            hex_maze[y][x] += Walls[step].value << PATH_OFFSET
            position += Walls[step].direction

    def display_maze(self) -> None:
        """Method to print the maze in the terminal.

        Calls private methods in the class in the right order.
        """
        ascii_maze = self._parse_hex()
        for row in ascii_maze:
            self._display_row(row)
        self._display_bottom()
