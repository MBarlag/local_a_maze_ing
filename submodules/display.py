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

    def _parse_hex() -> list[list[int]]:
        grid: list[list[int]]
        i = 0

        with open(output_file, "r") as file_obj:
            for line in file_obj:
                print(line)

