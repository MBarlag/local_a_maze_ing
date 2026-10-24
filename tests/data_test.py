"""[TODO:description]

[TODO:description]
"""


from submodules.abstract import Vector
from submodules.data import Maze, Room
from submodules.enums import Walls


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


def test_maze() -> None:
    pass


if __name__ == "__main__":
    test_room()

# with pytest.raises(Exception):
# 	# input for test
# maze = Maze(3, 3)
# room : Room = maze.cell
