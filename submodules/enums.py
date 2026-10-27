"""Enums related to Maze."""

from collections.abc import Generator
from enum import Enum, Flag

from submodules.abstract import Vector


class Step(Vector[int], Enum):
    """Steps are possible one step moves on 2D plane with Y axis looking down.

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
    def v(cls, vector: tuple[int, int] | Vector[int]) -> "Step":
        """Cast vector to Step if primitive vector."""
        for step in list(cls):
            if step.value == vector:
                return step
        raise Exception("Not a primitive step.")

    @property
    def opposite(self) -> "Step":
        """Opposite Step."""
        opposites: dict[Step, Step] = {
            Step.LEFT: Step.RIGHT,
            Step.UP: Step.DOWN,
            Step.RIGHT: Step.LEFT,
            Step.DOWN: Step.UP,
        }
        return opposites.get(self, Step.NOWHERE)


class Ways(Flag):
    """Direction config. Combines primitive W(est), S(outh), E(east), N(north).

    Attributes:
        W: Represents west way.
        S: Represents south way.
        E: Represents east way.
        N: Represents north way.
        EMPTY: Represents no ways.
        ALL: Represents all ways.
    """

    W = 0b1000
    S = 0b0100
    E = 0b0010
    N = 0b0001
    NONE = 0b0000
    ALL = 0b1111

    @property
    def hex(self) -> str:
        """Hex representation."""
        return hex(self.value)[2:]

    @property
    def count(self) -> int:
        """How many ways in the Ways configuration."""
        return len(list(self))

    @property
    def opposite(self) -> "Ways":
        """Opposite way."""
        opposites: dict[Ways, Ways] = {
            Ways.W: Ways.E,
            Ways.E: Ways.W,
            Ways.N: Ways.S,
            Ways.S: Ways.N,
        }
        return opposites.get(self, Ways.NONE)

    @classmethod
    def from_step(cls, step: Step) -> "Ways":
        """Converts a primitive step to a direction."""
        if step == Step.LEFT:
            return Ways.W
        elif step == Step.RIGHT:
            return Ways.E
        elif step == Step.UP:
            return Ways.N
        elif step == Step.DOWN:
            return Ways.S
        return Ways.NONE

    @property
    def as_step(self) -> Step:
        """Return Step corresponding to primitive Way."""
        if self == Ways.W:
            return Step.LEFT
        elif self == Ways.E:
            return Step.RIGHT
        elif self == Ways.N:
            return Step.UP
        elif self == Ways.S:
            return Step.DOWN
        return Step.NOWHERE

    def __str__(self) -> str:
        """Returns name of the configuration."""
        return repr(self)[6:].split(":")[0]

    def __iter__(self) -> Generator["Ways"]:
        """Yields all simple directions within the combined Way config."""
        for way in [Ways.W, Ways.S, Ways.E, Ways.N]:
            if way in self:
                yield way

    def __add__(self, other: "Ways | int") -> "Ways":
        """Adds to current Way config another Way config."""
        return self | Ways(other)

    def __radd__(self, other: "Ways | int") -> "Ways":
        """Same as __add__."""
        return self | Ways(other)

    def __sub__(self, other: "Ways | int") -> "Ways":
        """Binary subtacts from current Way config another config."""
        return self ^ Ways(other)

    def __rsub__(self, other: "Ways | int") -> "Ways":
        """Same as __sub__."""
        return Ways(other) ^ self
