import pytest

from mazegen.abstract import Vector
from submodules.config import Config
from mazegen.data import Maze, Room
from submodules.display import MazePrinter
from mazegen.enums import Step, Ways
from mazegen.generator import MazeGenerator


def test_maze() -> None:
    with pytest.raises(ValueError, match="negative") as e:
        Maze(-3, 3)
    with pytest.raises(ValueError, match="zero") as e2:
        Maze(0, 3)
    assert "Maze" in str(e2.value)
    assert "Maze" in str(e.value)
    config = Config("tests/good_config.txt").parse_config()
    config["output_file"] = "T1.txt"
    print(config)
    maze_gen = MazeGenerator(**config)
    maze = maze_gen.generate()
    if not maze:
        raise Exception("Error generating.")
    print(
        maze.view(
            lambda x: (
                "0" if x.path_hint is Step.NOWHERE else x.path_hint.name[0]
            )
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

    room.walls -= Ways.W
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
