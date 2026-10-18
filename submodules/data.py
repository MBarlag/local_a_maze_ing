
from submodules.abstract import Cell, Grid, Vector
from submodules.enums import Wall


class Room(Cell):
    
    def __init__(self, y: int, x: int, ref: Grid):
        super().__init__(y, x, ref)
        self.visited = False
        self.walls = Wall.BLOCK
        self.blocked = False

    @property
    def surrounded(self) -> Wall:
        surrounded = Wall.BLOCK
        for wall in Wall.BLOCK:
            neighbour = self + wall.direction
            if neighbour is None:
                continue
            if wall.opposite not in neighbour.walls:
                surrounded -= wall
        return surrounded

    @property
    def valid(self) -> bool:
        return self.walls == sum(self.surrounded)

    def break_wall(self, to_break: Wall) -> None:
        if to_break in self.walls:
            self.walls -= to_break
            neighbour = self + to_break.direction
            if neighbour is None:
                raise ValueError("Can't break borders of the maze")
            neighbour.walls -= to_break.opposite
        else:
            raise ValueError("Walls requested don't exist")


class Maze(Grid):

    def __init__(self, width: int, height: int, 
                 entry: Vector[int],
                 exit: Vector[int]) -> None:
        super().__init__(width, height, Room)
        self._set_entry(entry)
        self._set_exit(exit)

    @property
    def room(self) -> Room:
        return self._grid[0][0]

    @property
    def entry(self) -> Vector[int]:
        return self._entry

    def _set_entry(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError("Coordinates are not reachable")
        self._entry = coord

    @property
    def exit(self) -> Vector[int]:
        return self._exit

    def _set_exit(self, coord: Vector[int]) -> None:
        if self.cant_reach(*coord):
            raise ValueError("Coordinates are not reachable")
        self._exit = coord
