from submodules.abstract import Vector
from submodules.config import Config
from submodules.data import Maze, Room
from submodules.display import MazePrinter
from submodules.enums import Move, Walls
from submodules.generator import MazeGenerator


def test_maze() -> None:
    config = Config("tests/good_config.txt").parse_config()
    config["output_file"] = "T1.txt"
    print(config)
    maze_gen = MazeGenerator(**config)
    maze = maze_gen.generate()
    if not maze:
        raise Exception("Error generating.")
    print(
        maze.view(
            lambda x: "0" if x.to_exit is Move.NOWHERE else x.to_exit.name[0]
        )
    )
    printer = MazePrinter(**config)
    printer.display_maze()


def test_room() -> None:
    maze = Maze(3, 3, Vector(0, 0), Vector(0, 0))
    assert maze.valid == False
    maze = Maze(3, 3, Vector(0, 0), Vector(1, 2))
    assert maze.valid == True

    room: Room = maze.room

    # room[0, 0].connect_with(Walls.S)
    assert room.valid == True
    assert maze.valid == True

    room.walls -= Walls.W
    assert room.valid == False
    assert maze.valid == False

    # with pytest.raises(ValueError):
    #     room[0, 0].connect_with(Walls.N)

    assert room.visited == False
    room.visited = True
    assert room.visited == True


# with pytest.raises(Exception):
# 	# input for test
# maze = Maze(3, 3)
# room : Room = maze.cell
