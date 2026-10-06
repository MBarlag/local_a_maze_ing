from data import *
import pytest


def test_room():
	maze = Maze(3, 3)
	assert maze.valid == True

	room : Room = maze.cell
    
	room(0, 0).break_wall(Wall.S)
	assert room.valid == True

	room.walls -= Wall.W
	assert room.valid == False



if __name__ == '__main__':
    test_room()

# with pytest.raises(Exception):
# 	# input for test
# maze = Maze(3, 3)
# room : Room = maze.cell