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
        with open(self.output_file, "r") as file_obj:
            for line in file_obj:
                line = line.strip()
                if not line:
                    break
                hex_maze.append([int(char, 16) for char in line])

        self._mark_point(16, hex_maze)
        self._mark_point(32, hex_maze)
        return hex_maze

    def _mark_point(self, point_type: int, hex_maze: list[list[int]]) -> None:
        """With the entry/exit coordinates, this method changes this cell in
        hex_maze by adding 16 for entry and 32 for exit.

        Args:
            point_type (int): Is 16 for entry or 32 for exit.
            hex_maze (list[list[int]]): Holds maze cells and entry/exit points.
        """

        coord: tuple[int, int]
        if point_type == 16:
            coord = self._parse_coords(self.entry)
        elif point_type == 32:
            coord = self._parse_coords(self.exit)
        else:
            raise ValueError
        # This should never happen, so do we need this?
        # And how to handle the error?

        x, y = coord
        hex_maze[y][x] += point_type

    def _display_row(self, hex_row: list[int]) -> None:
        """Prints the North and West walls of a maze row.
        Closes the row with a + and │ character.

        Args:
            hex_row (list[int]): One line of hexadecimal characters.
        """

        north = 1
        west = 8
        entry = 16
        exit = 32
        for cell in hex_row:
            print("+", end="")
            if cell & north:
                print("---", end="")
            else:
                print("   ", end="")
        print("+")

        for cell in hex_row:
            if cell & west:
                print("|", end="")
            else:
                print(" ", end="")

            if cell & entry:
                print(" A ", end="")
            elif cell & exit:
                print(" B ", end="")
            else:
                print("   ", end="")
        print("|")

    def _display_bottom(self) -> None:
        """Prints the closing South walls of the maze.
        """

        for _ in range(self.width):
            print("+---", end="")
        print("+")

    def display_maze(self) -> None:
        """Calls private methods in the class in the right order to
        print the maze in the terminal.
        """

        ascii_maze = self._parse_hex()
        for row in ascii_maze:
            self._display_row(row)
        self._display_bottom()
