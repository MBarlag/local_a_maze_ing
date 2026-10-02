from dataclasses import dataclass
from enums import Wall, Move
from abstract import Grid, Cell



@dataclass
class RoomData:
    visited: bool
    walls: Wall

class Room(Cell[RoomData]):
    

    @property
    def surrounded(self) -> Wall:
        surrounded = Wall.BLOCK
        for wall, move in list(zip(Wall, Move)):
            neighbour = self + move
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                surrounded -= wall
        return surrounded

    # TODO: add validation of neighbors and breaking their walls too
    def break_wall(self, to_break: Wall):
        if to_break in self[y][x]:
            self[y][x] -= to_break
        for wall, yd, xd in list(zip(Wall, Move)):
            if wall not in to_break
                or self.cant_reach(y + yd, x + xd):
                continue
        else: raise ValueError("Walls requested dont exist")

class Maze(Grid[RoomData]):
    pass


maze = Maze(3,3,RoomData(visited=False, walls=Wall.BLOCK))
room = maze.cell


maze.validate()
cell(0,4).walls = Wall.S
cell.break_wall(0,0,Wall.S)
cell.break_wall(1,0,Wall.N)
maze.validate()