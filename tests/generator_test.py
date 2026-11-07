import random
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import FrozenInstanceError
from functools import partial
from random import randint
from typing import Any

import pytest
from pydantic import ValidationError

from a_maze_ing import format_pydantic_error
from submodules.abstract import Cell, Grid, Vector
from submodules.config import ConfigParser, MazeConfig
from submodules.data import MazeError
from submodules.display import MazePrinter
from submodules.enums import Ways
from submodules.generator import (
    P42_MIN_HEIGHT,
    P42_MIN_WIDTH,
    MazeGenerator,
    MazeGenError,
)
from submodules.safe_types import IntVector
from tests.maze_analyzer import Maze as MAZE
from tests.maze_analyzer import analyze, render


@contextmanager
def pydantic_pretty() -> Generator[None]:
    try:
        yield
    except ValidationError as e:
        pytest.fail(format_pydantic_error(e))


def test_valid_config_pipeline() -> None:
    config = ConfigParser("tests/good_config.txt").parse()
    maze_gen = MazeGenerator(**config)
    # maze_gen.generate()
    assert type(maze_gen.entry) == Vector
    assert type(maze_gen.entry.x) == int
    with pytest.raises(FrozenInstanceError):
        maze_gen.entry.x = 3


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


RAND_WIDTH = 50
RAND_HEIGHT = 50
PERFECT_TRIES = 50
PACMAN_TRIES = 50


# ALWAYS FAILS: 2x2
# if 2x3 or 3x2: we can always make them empty inside to pass the pacman
#
def test_random_pacman(subtests: pytest.Subtests) -> None:
    for i in range(PACMAN_TRIES):
        random.seed()
        width = randint(0, RAND_WIDTH)
        height = randint(0, RAND_HEIGHT)
        with subtests.test(f"{width}x{height}"), pydantic_pretty():
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
            dict_config: dict[str, Any] = {
                "width": f"{width}",
                "height": f"{height}",
                "output_file": "tests/output/imperfect.txt",
                "perfect": "False",
            }
            config = MazeConfig(entry=entry, exit=exit, **dict_config)

            if width == 0 and height != 1 or width != 1 and height == 0:
                with pytest.raises(ValueError, match="zero"):
                    maze_gen = MazeGenerator(
                        entry=entry, exit=exit, **dict_config
                    )
                    maze = maze_gen.generate()
                continue
            if entry == exit and width != 1 and height != 1:
                with pytest.raises(MazeError, match="entry == exit"):
                    maze_gen = MazeGenerator(
                        entry=entry, exit=exit, **dict_config
                    )
                    maze = maze_gen.generate()
                continue
            if width == 1 or height == 1:
                with pytest.raises(MazeGenError, match="equal to 1"):
                    maze_gen = MazeGenerator(
                        entry=entry, exit=exit, **dict_config
                    )
                    maze = maze_gen.generate()
                continue
            if width == 2 and height == 2:
                with pytest.raises(MazeGenError, match="Failed"):
                    maze_gen = MazeGenerator(
                        entry=entry, exit=exit, **dict_config
                    )
                    maze = maze_gen.generate()
                continue
            # if 7 <= width <= 8 and height >= 5:
            #     with pytest.raises(MazeGenError, match="Failed"):
            #         maze_gen = MazeGenerator(
            #             entry=entry, exit=exit, **dict_config
            #         )
            #         maze = maze_gen.generate()
            #     continue
            # if 5 <= height <= 5 and width >= 7:
            #     with pytest.raises(MazeGenError, match="Failed"):
            #         maze_gen = MazeGenerator(
            #             entry=entry, exit=exit, **dict_config
            #         )
            #         maze = maze_gen.generate()
            #     continue
            maze_gen = MazeGenerator(entry=entry, exit=exit, **dict_config)
            maze = maze_gen.generate()
            if not maze:
                raise Exception("Maze did not generate.")
            walls = Grid(
                maze.width,
                maze.height,
                from_file=config.output_file,
                on_each_char=lambda x: Ways(int(x, 16)),
            )
            print(walls)
            printer = MazePrinter(**config.as_dict)
            printer.display_maze()
            print(f"SEED: {maze_gen.seed=}")
            m = MAZE.from_file(config.output_file)
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
        with (
            subtests.test(f"{width}x{height}"),
            pydantic_pretty(),
        ):
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
            dict_config: dict[str, Any] = {
                "width": f"{width}",
                "height": f"{height}",
                "output_file": "tests/output/perfect.txt",
                "perfect": "True",
            }
            config = MazeConfig(entry=entry, exit=exit, **dict_config)

            if width == 0 or height == 0:
                with pytest.raises(ValueError, match="zero"):
                    maze_gen = MazeGenerator(
                        entry=entry, exit=exit, **dict_config
                    )
                continue
            if entry == exit:
                with pytest.raises(MazeError, match="entry == exit"):
                    maze_gen = MazeGenerator(
                        entry=entry, exit=exit, **dict_config
                    )
                continue
            if entry == exit and width != 1 and height != 1:
                with pytest.raises(MazeError, match="entry == exit"):
                    maze_gen = MazeGenerator(
                        entry=entry, exit=exit, **dict_config
                    )
                    maze = maze_gen.generate()
                continue
            # if 7 <= width <= 8 and height >= 5:
            #     with pytest.raises(MazeGenError, match="Failed"):
            #         maze_gen = MazeGenerator(
            #             entry=entry, exit=exit, **dict_config
            #         )
            #         maze = maze_gen.generate()
            #     continue
            # if 5 <= height <= 5 and width >= 7:
            #     with pytest.raises(MazeGenError, match="Failed"):
            #         maze_gen = MazeGenerator(
            #             entry=entry, exit=exit, **dict_config
            #         )
            #         maze = maze_gen.generate()
            #     continue
            maze_gen = MazeGenerator(entry=entry, exit=exit, **dict_config)
            maze = maze_gen.generate()
            if not maze:
                raise Exception("Maze did not generate.")
            walls = Grid(
                maze.width,
                maze.height,
                from_file=config.output_file,
                on_each_char=lambda x: Ways(int(x, 16)),
            )
            print(walls)
            printer = MazePrinter(**config.as_dict)
            printer.display_maze()
            print(f"SEED: {maze_gen.seed=}")
            m = MAZE.from_file(config.output_file)
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
    dict_config: dict[str, str] = {
        "width": f"{width}",
        "height": f"{height}",
        "entry": "0,0",
        "exit": f"{width - 1},{height - 1}",
        "output_file": "tests/output/imperfect.txt",
        "perfect": "False",
    }
    config = MazeConfig(**dict_config)
    maze_gen = MazeGenerator(**vars(config))
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
