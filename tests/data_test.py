import pytest

from submodules.data import Maze, Room
from submodules.abstract import Vector
from submodules.enums import Wall


def test_room() -> None:
    maze = Maze(3, 3, Vector(0, 0), Vector(0, 1))
    assert maze.valid == True

    room : Room = maze.room
    
    room(0, 0).break_wall(Wall.S)
    assert room.valid == True
    assert maze.valid == True

    room.walls -= Wall.W
    assert room.valid == False
    assert maze.valid == False

    with pytest.raises(ValueError):
        room(0, 0).break_wall(Wall.N)

    assert room.visited == False
    room.visited = True
    assert room.visited == True


if __name__ == '__main__':
    test_room()

# with pytest.raises(Exception):
# 	# input for test
# maze = Maze(3, 3)
# room : Room = maze.cell