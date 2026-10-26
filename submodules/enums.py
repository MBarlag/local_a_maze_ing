"""Enums related to Maze: one-step moves and wall combinations."""

from collections.abc import Generator
from enum import Enum, Flag

from submodules.abstract import Vector


class Move(Vector[int], Enum):
    """Enum for possible one step moves on 2D plane with Y axis looking down.

    Attributes:
        LEFT: Corresponds to Vector(-1, 0)
        DOWN: Corresponds to Vector(0, 1)
        RIGHT: Corresponds to Vector(1, 0)
        UP: Corresponds to Vector(0, -1)
        NOWHERE: Corresponds to Vector(0, 0)
    """

    LEFT = -1, 0
    DOWN = 0, 1
    RIGHT = 1, 0
    UP = 0, -1
    NOWHERE = 0, 0

    @classmethod
    def v(cls, vector: tuple[int, int] | Vector[int]) -> "Move":
        """Translation for mypy: get Move that matches a vector."""
        for move in list(cls):
            if move.value == vector:
                return move
        raise Exception("Not a primitive move.")

    # def __iter__(self) -> Iterator[int]:
    #    return iter(self.value)
    # def __eq__(self, other: Vector[int] | type["Move"] | tuple[int, int]):
    #
    #   y, x = other
    #   return y == self.y and x == self.x


class Walls(Flag):
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
    def opposite(self) -> "Walls":
        """Get the opposite Wall."""
        opposites: dict[Walls, Walls] = {
            Walls.W: Walls.E,
            Walls.E: Walls.W,
            Walls.N: Walls.S,
            Walls.S: Walls.N,
        }
        return opposites.get(self, Walls.EMPTY)

    @property
    def direction(self) -> Move:
        """Direction the Wall is located at."""
        if self == Walls.W:
            return Move.LEFT
        elif self == Walls.E:
            return Move.RIGHT
        elif self == Walls.N:
            return Move.UP
        elif self == Walls.S:
            return Move.DOWN
        return Move.NOWHERE

    def __str__(self) -> str:
        """Return name of the configuration for example "W|S"."""
        return repr(self)[7:].split(":")[0]

    @classmethod
    def __getitem__(cls, repr: str) -> "Walls":
        """Get basic Walls members by their names. Walls["W"] => Walls.W."""
        allowed_values = {
            "W": Walls.W,
            "S": Walls.S,
            "E": Walls.E,
            "N": Walls.N,
        }
        if repr in allowed_values:
            return allowed_values[repr]
        else:
            raise ValueError("Wrong representation.")

    def __iter__(self) -> Generator["Walls"]:
        """Iterate over the four single walls in the order W, S, E, N.

        Yields:
            The single wall if it is part of this combination,
            Walls.EMPTY otherwise. Always yields four values."""
        for wall in [Walls.W, Walls.S, Walls.E, Walls.N]:
            if wall in self:
                yield wall
            else:
                yield Walls.EMPTY

    def __add__(self, other: "Walls | int") -> "Walls":
        """Adds to current wall state another wall state (bitwise)."""
        return self | Walls(other)

    def __radd__(self, other: "Walls | int") -> "Walls":
        """Same as __add__, with walls on the right of +."""
        return self | Walls(other)

    def __sub__(self, other: "Walls | int") -> "Walls":
        """Subtacts from current wall state another state (bitwise)."""
        return self ^ Walls(other)

    def __rsub__(self, other: "Walls | int") -> "Walls":
        """Same as __sub__, with walls on the right of -."""
        return Walls(other) ^ self
