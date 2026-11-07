# Run from project root as a module: python3 -m tests.display_test

from mazegen.config import ConfigParser
from submodules.display import MazePrinter
from mazegen.generator import MazeGenerator


# def test_small_maze() -> None:
#     config: dict[str, str] = {
#         "width": "3",
#         "height": "3",
#         "entry": "0,0",
#         "exit": "2,2",
#         "output_file": "tests/output/hex_small_maze.txt",
#     }
#     printer = MazePrinter(**config)
#     printer.display_maze()



# def test_big_maze() -> None:
#     config: dict[str, str] = {
#         "width": "25",
#         "height": "20",
#         "entry": "1,1",
#         "exit": "19,14",
#         "output_file": "tests/output/hex_big_maze.txt",
#     }
#     printer = MazePrinter(**config)
#     printer.display_maze()


# def test_gen_maze() -> None:
#     config = ConfigParser("tests/good_config.txt").parse()
#     maze_gen = MazeGenerator(**config)
#     maze_gen.generate()
#     printer = MazePrinter(**config)
#     printer.display_maze()


# if __name__ == "__main__":
#     # test_small_maze()
#     # test_big_maze()
#     test_gen_maze()
