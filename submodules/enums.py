from enum import Enum, Flag

class Move(Enum):
    LEFT    = (0, -1)
    DOWN    = (1, 0)
    RIGHT   = (0, 1)
    UP      = (-1, 0)
    NOWHERE = (0, 0)

class Wall(Flag):
    W =     0b1000
    S =     0b0100
    E =     0b0010
    N =     0b0001
    EMPTY = 0b0000
    BLOCK = 0b1111


    @property.getter
    def opposite(self):
        opposites = \
            {Wall.W: Wall.E,
            Wall.E: Wall.W,
            Wall.N: Wall.S,
            Wall.S: Wall.N}
        return opposites.get(self, Wall.EMPTY)

    @property.getter
    def direction(self) -> Move:
        if self == Wall.W:
            return Move.LEFT
        elif self == Wall.E:
            return Move.RIGHT
        elif self == Wall.N:
            return Move.UP
        elif self == Wall.S:
            return Move.DOWN
    
    def __iter__(self):
        for wall in [Wall.W, Wall.S, Wall.E, Wall.N]:
            if wall in self:
                yield wall
            else: yield Wall.EMPTY
    def __add__(self, other: Flag | int):
        return self | Wall(other)
    def __radd__(self, other: Flag | int):
            return self | Wall(other)
    def __sub__(self, other: Flag | int):
        return self ^ Wall(other)
    def __rsub__(self, other: Flag | int):
        return Wall(other) ^ self
