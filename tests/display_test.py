# Run from project root as a module: python3 -m tests.display_test
from submodules.display import MazePrinter


def test_small_maze() -> None:
    config: dict[str, str] = {"width": "3", "height": "3",
                              "entry": "0,0", "exit": "2,2",
                              "output_file": "tests/hex_small_maze.txt"}
    printer = MazePrinter(**config)
    printer.display_maze()


def test_big_maze() -> None:
    config: dict[str, str] = {"width": "25", "height": "20",
                              "entry": "0,0", "exit": "24,19",
                              "output_file": "tests/hex_big_maze.txt"}
    printer = MazePrinter(**config)
    printer.display_maze()


if __name__ == '__main__':
    test_small_maze()
    test_big_maze()
