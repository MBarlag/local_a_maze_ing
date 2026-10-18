"""Enums related to Maze.

[TODO:description]
"""

from collections.abc import Generator
from enum import Enum, Flag

from submodules.abstract import Vector


class Move(Vector[int], Enum):
    """Enum for possible one step moves on 2D plane with Y axis looking down.

    Attributes:
        LEFT: Corresponds to Vector(0, -1)
        DOWN: Corresponds to Vector(1, 0)
        RIGHT: Corresponds to Vector(0, 1)
        UP: Corresponds to Vector(-1, 0)
        NOWHERE: Corresponds to Vector(0, 0)
    """

    LEFT = 0, -1
    DOWN = 1, 0
    RIGHT = 0, 1
    UP = -1, 0
    NOWHERE = 0, 0

    # def __iter__(self) -> Iterator[int]:
    #    return iter(self.value)
    # def __eq__(self, other: Vector[int] | type["Move"] | tuple[int, int]):
    #
    #   y, x = other
    #   return y == self.y and x == self.x


class Wall(Flag):
    """Enum representing combination of wall locations.

    Attributes:
        W: Represents west wall.
        S: Represents south wall.
        E: Represents east wall.
        N: Represents north wall.
        EMPTY: Represents no walls.
        BLOCK: Represents all walls.
    """

    W = 0b1000
    S = 0b0100
    E = 0b0010
    N = 0b0001
    EMPTY = 0b0000
    BLOCK = 0b1111

    @property
    def opposite(self) -> "Wall":
        """Opposite wall."""
        opposites: dict[Wall, Wall] = {
            Wall.W: Wall.E,
            Wall.E: Wall.W,
            Wall.N: Wall.S,
            Wall.S: Wall.N,
        }
        return opposites.get(self, Wall.EMPTY)

    @property
    def direction(self) -> Move:
        """Direction the Wall is located at."""
        if self == Wall.W:
            return Move.LEFT
        elif self == Wall.E:
            return Move.RIGHT
        elif self == Wall.N:
            return Move.UP
        elif self == Wall.S:
            return Move.DOWN
        return Move.NOWHERE

    def __iter__(self) -> Generator["Wall"]:
        """Yields all the base wall states within the combined wall state."""
        for wall in [Wall.W, Wall.S, Wall.E, Wall.N]:
            if wall in self:
                yield wall
            else:
                yield Wall.EMPTY

    def __add__(self, other: "Wall | int") -> "Wall":
        """Adds to current wall state another wall state."""
        return self | Wall(other)

    def __radd__(self, other: "Wall | int") -> "Wall":
        """Same as __add__."""
        return self | Wall(other)

    def __sub__(self, other: "Wall | int") -> "Wall":
        """Subtacts from current wall state another state."""
        return self ^ Wall(other)

    def __rsub__(self, other: "Wall | int") -> "Wall":
        """Same as __sub__."""
        return Wall(other) ^ self
