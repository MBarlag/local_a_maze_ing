from pydantic import BaseModel

class MazePrinter(BaseModel):
    """ Renders and displays hexadecimal file as readable maze in terminal.

    Attributes:
        width (int): Number of cells per row.
        height (int): Number of rows.
        output_file (str): Path to the hexadecimal file.
    """

    width: int
    height: int
    output_file: str

        