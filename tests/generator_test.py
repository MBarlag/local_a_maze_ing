import random
from copy import copy
from dataclasses import FrozenInstanceError
from functools import partial
from random import randint
from typing import Any

import pytest

from submodules.abstract import Cell, Grid, Vector
from submodules.config import Config
from submodules.display import MazePrinter
from submodules.enums import Ways
from submodules.generator import P42_MIN_HEIGHT, P42_MIN_WIDTH, MazeGenerator
from submodules.safe_types import IntVector
from tests.maze_analyzer import Maze as MAZE
from tests.maze_analyzer import analyze, render


def gen_configs() -> Any:
    BAD_CONFIGS = []
    bad_config = Config("tests/bad_config.txt").parse_config()
    good_config = Config("tests/good_config.txt").parse_config()
    for k, v in list(bad_config.items()):
        conf = copy(good_config)
        conf[k] = v
        BAD_CONFIGS.append(conf)
    # print(BAD_CONFIGS)
    return BAD_CONFIGS


BAD_CONFIGS = gen_configs()


def test_valid_config_pipeline() -> None:
    config = Config("tests/good_config.txt").parse_config()
    maze_gen = MazeGenerator(**config)
    # maze_gen.generate()
    assert type(maze_gen.entry) == Vector
    assert type(maze_gen.entry.x) == int
    with pytest.raises(FrozenInstanceError):
        maze_gen.entry.x = 3


@pytest.mark.parametrize("config", BAD_CONFIGS)
def test_invalid_config_pipeline(config: dict[str, str]) -> None:
    with pytest.raises((ValueError, TypeError)):
        print(config)
        MazeGenerator(**config)


def pick_valid(
    grid: Grid[bool, Cell[bool]] | None,
) -> tuple[IntVector, IntVector]:
    if not grid or (grid.width == 1 and grid.height == 1):
        return Vector(0, 0), Vector(0, 0)
    rand_height = partial(randint, 0, grid.height - 1)
    rand_width = partial(randint, 0, grid.width - 1)

    entry = Vector(rand_width(), rand_height())
    exit = Vector(rand_width(), rand_height())
    while (
        grid[entry].value is True or grid[exit].value is True or entry == exit
    ):
        entry = Vector(rand_width(), rand_height())
        exit = Vector(rand_width(), rand_height())
    return entry, exit


RAND_WIDTH = 15
RAND_HEIGHT = 15
PERFECT_TRIES = 1000
PACMAN_TRIES = 1000


# ALWAYS FAILS: 2x2
# if 2x3 or 3x2: we can always make them empty inside to pass the pacman
#
def test_random_pacman(subtests: pytest.Subtests) -> None:
    for i in range(PACMAN_TRIES):
        random.seed()
        width = randint(0, RAND_WIDTH)
        height = randint(0, RAND_HEIGHT)
        with subtests.test(f"{width}x{height}"):
            pattern = Grid(
                7, 5, from_file="42.txt", on_each_char=lambda c: c == "f"
            )
            grid = None
            try:
                grid = Grid(width, height, default=False)
                if width >= P42_MIN_WIDTH and height >= P42_MIN_HEIGHT:
                    x = (width - pattern.width) // 2 + 1 - width % 2
                    y = (height - pattern.height) // 2 + 1 - height % 2
                    origin = grid[x, y]
                    for cell in pattern:
                        offset = cell.as_vector
                        origin[offset].value = cell.value
            except Exception:
                pass
            entry, exit = pick_valid(grid)
            config: dict[str, str] = {
                "width": f"{width}",
                "height": f"{height}",
                "output_file": "imperfect.txt",
                "perfect": "False",
            }
            maze_gen = MazeGenerator(entry=entry, exit=exit, **config)
            maze = maze_gen.generate()
            if not maze:
                raise Exception("Maze did not generate.")
            walls = Grid(
                maze.width,
                maze.height,
                from_file=config["output_file"],
                on_each_char=lambda x: Ways(int(x, 16)),
            )
            print(walls)
            config["entry"] = str(entry).strip("()")
            config["exit"] = str(exit).strip("()")
            printer = MazePrinter(**config)
            printer.display_maze()
            print(f"SEED: {maze_gen.seed=}")
            m = MAZE.from_file(config["output_file"])
            report = analyze(m)
            text = render(report, 2, 2)
            print(text)
            assert report.incoherent != False
            assert report.loops >= 2
            assert report.dead_ends[0] <= 2
            assert report.disconnected_corridors != True
            assert report.unreachable_key_cells != True
            assert "Pac-Man-USABLE" in text


def test_random_perfect(subtests: pytest.Subtests) -> None:
    for i in range(PERFECT_TRIES):
        random.seed()
        width = randint(0, RAND_WIDTH)
        height = randint(0, RAND_HEIGHT)
        with subtests.test(f"{width}x{height}"):
            pattern = Grid(
                7, 5, from_file="42.txt", on_each_char=lambda c: c == "f"
            )
            grid = None
            try:
                grid = Grid(width, height, default=False)
                if width >= P42_MIN_WIDTH and height >= P42_MIN_HEIGHT:
                    x = (width - pattern.width) // 2 + 1 - width % 2
                    y = (height - pattern.height) // 2 + 1 - height % 2
                    origin = grid[x, y]
                    for cell in pattern:
                        offset = cell.as_vector
                        origin[offset].value = cell.value
            except Exception:
                pass
            entry, exit = pick_valid(grid)
            config: dict[str, str] = {
                "width": f"{width}",
                "height": f"{height}",
                "output_file": "perfect.txt",
                "perfect": "True",
            }
            maze_gen = MazeGenerator(entry=entry, exit=exit, **config)
            maze = maze_gen.generate()
            if not maze:
                raise Exception("Maze did not generate.")
            walls = Grid(
                maze.width,
                maze.height,
                from_file=config["output_file"],
                on_each_char=lambda x: Ways(int(x, 16)),
            )
            print(walls)
            config["entry"] = str(entry).strip("()")
            config["exit"] = str(exit).strip("()")
            printer = MazePrinter(**config)
            printer.display_maze()
            print(f"SEED: {maze_gen.seed=}")
            m = MAZE.from_file(config["output_file"])
            report = analyze(m)
            text = render(report, 2, 2)
            print(text)
            assert not report.incoherent
            assert report.loops == 0
            assert not report.disconnected_corridors
            assert "PERFECT maze" in text


def debug() -> None:
    width = 500
    height = 500
    config: dict[str, str] = {
        "width": f"{width}",
        "height": f"{height}",
        "entry": "0,0",
        "exit": f"{width - 1},{height - 1}",
        "output_file": "imperfect.txt",
        "perfect": "False",
    }
    maze_gen = MazeGenerator(**config)
    maze = maze_gen.generate()
    if not maze:
        raise Exception("Maze did not generate.")
    # grid = Grid(
    #     maze.width,
    #     maze.height,
    #     from_file=config["output_file"],
    #     on_each_char=lambda x: Ways(int(x, 16)),
    # )
    # print(grid)
    # printer = MazePrinter(**config)
    # printer.display_maze()
    # m = MAZE.from_file(config["output_file"])
    # report = analyze(m)
    # print(render(report, 2, 2))


# if __name__ == "__main__":
#     debug()
