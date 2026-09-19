from pydantic import BaseModel


class MazePrinter(BaseModel):
    """Parses and displays hexadecimal file as readable maze in terminal.

    Attributes:
        width (int): Number of cells per row.
        height (int): Number of rows.
        entry (str): Coordinates of entry point.
        exit (str): Coordinates of exit point.
        output_file (str): Path to the hexadecimal file.
    """

    width: int
    height: int
    entry: str
    exit: str
    output_file: str

    @staticmethod
    def _parse_coords(coord: str) -> tuple[int, int]:
        """Converts coordinate string into (x, y) tuple.

        Args:
            coord (str): _description_

        Returns:
            tuple[int, int]: _description_
        """
        xy = coord.split(",")
        x = int(xy[0])
        y = int(xy[1])
        return x, y

    def _parse_hex(self) -> list[list[int]]:
        """Reads maze lines from hexadecimal file to a list of list[int].

        Returns:
            list[list[int]]: Holds maze cells and entry/exit points
            in ints of 0 until 17.
        """
        hex_maze: list[list[int]] = []
        with open(self.output_file, "r") as file_obj:
            for line in file_obj:
                line = line.strip()
                if not line:
                    break
                hex_maze.append([int(char, 16) for char in line])

        self._mark_point(16, hex_maze)
        self._mark_point(17, hex_maze)
        return hex_maze

    def _mark_point(self, point_type: int, hex_maze: list[list[int]]) -> None:
        coord: tuple
        if point_type == 16:
            coord = self._parse_coords(self.entry)
        elif point_type == 17:
            coord = self._parse_coords(self.exit)
        else:
            raise ValueError

        x, y = coord
        hex_maze[y].insert(x + 1, point_type)   # This still needs a fix, because by printing A and B, it moves the row 1 character.
        # hex_maze[y][x] = point_type

    def _display_row(self, hex_row: list[int]) -> None:
        """Prints the North and West walls of a maze row.
        Closes the row with a + and │ character.

        Args:
            hex_row (list[int]): One line of hexadecimal characters.
        """
        for top_type in hex_row:
            if top_type in (0, 2, 4, 6):
                print("   ", end="")
            elif top_type in (1, 3, 5, 7):
                print("---", end="")
            elif top_type in (8, 10, 12, 14):
                print("+  ", end="")
            elif top_type in (9, 11, 13, 15):
                print("+--", end="")
        print("+")

        for cell_type in hex_row:
            if cell_type in (0, 1, 2, 3, 4, 5, 6, 7):
                print("   ", end="")
            elif cell_type in (8, 9, 10, 11, 12, 13, 14, 15):
                print("│  ", end="")
            elif cell_type == 16:
                print("A", end="")
            elif cell_type == 17:
                print("B", end="")
        print("│")

    def _display_bottom(self, hex_maze: list[list[int]]) -> None:   # Used a different parsing technique: comparing at bit level. More readable?
        """Prints the closing South walls of the maze.

        Args:
            hex_maze (list[list[int]]): Used to find last row.
        """
        west = 8
        bottom_row: list[int] = hex_maze[self.height - 1]

        for bottom_type in bottom_row:
            if bottom_type & west:
                print("+--", end="")
            else:
                print("---", end="")
        print("+")

    def display_maze(self) -> None:
        ascii_maze = self._parse_hex()
        for row in ascii_maze:
            self._display_row(row)
        self._display_bottom(ascii_maze)
