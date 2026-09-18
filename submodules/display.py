from pydantic import BaseModel

class MazePrinter(BaseModel):
    """ Parses and displays hexadecimal file as readable maze in terminal.

    Attributes:
        width (int): Number of cells per row.
        height (int): Number of rows.
        output_file (str): Path to the hexadecimal file.
    """

    width: int
    height: int
    output_file: str

    def _parse_hex(self) -> list[list[int]]:
        """Reads maze lines from hexadecimal file to a list of list[int].

        Returns:
            list[list[int]]: Holds the grid in ints of 0 until 15.
        """
        hex_maze: list[list[int]] = []
        with open(self.output_file, "r") as file_obj:
            for line in file_obj:
                line = line.strip()
                if not line:
                    break
                hex_maze.append([int(char, 16) for char in line])
        return hex_maze

    def display_row(self, hex_row: list[int]) -> None:
        for top_type in hex_row:
            if top_type in (0):
                print("   ", end="")
            if top_type in (1):
                print("---", end="")

    
            if top_type in (1, 5):
                print("─--", end="")
            elif top_type == 3:
                print("--┐", end="")
            elif top_type in (7, 9, 11, 13, 15):
                print("┌--", end="")
            else:
                print(" x ", end="")
        print()

        for cell_type in hex_row:
            if cell_type in (0, 1, 4, 5):
                print("   ", end="")
            elif cell_type in (2, 3, 6, 7):
                print("  │", end="")
            elif cell_type in (8, 9, 12, 13):
                print("│  ", end="")
            elif cell_type in (10, 11, 14, 15):
                print("│ │", end="")
        print()

