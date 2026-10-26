import random
from copy import copy
from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from submodules.abstract import Grid, Vector
from submodules.config import Config
from submodules.display import MazePrinter
from submodules.enums import Walls
from submodules.generator import MazeGenerator
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
    print(BAD_CONFIGS)
    return BAD_CONFIGS


BAD_CONFIGS = gen_configs()


def test_valid_config_pipeline() -> None:
    config = Config("tests/good_config.txt").parse_config()
    maze_gen = MazeGenerator(**config)
    assert type(maze_gen.entry) == Vector
    assert type(maze_gen.entry.x) == int
    with pytest.raises(FrozenInstanceError):
        maze_gen.entry.x = 3


@pytest.mark.parametrize("config", BAD_CONFIGS)
def test_invalid_config_pipeline(config: dict[str, str]) -> None:
    with pytest.raises((ValueError, TypeError)):
        print(config)
        MazeGenerator(**config)


def test_generate_pacman(subtests: pytest.Subtests) -> None:
    width = random.randint(7, 20)
    height = random.randint(5, 20)
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
    grid = Grid(
        maze.width,
        maze.height,
        from_file=config["output_file"],
        on_each_char=lambda x: Walls(int(x, 16)),
    )
    print(grid)

    m = MAZE.from_file(config["output_file"])
    report = analyze(m)
    print(render(report, 2, 2))
    with subtests.test("coherent"):
        assert report.incoherent != False
    with subtests.test("loops-check"):
        assert report.loops >= 2
    with subtests.test("deadends"):
        assert report.dead_ends[0] <= 2
    with subtests.test("not-disconnected"):
        assert report.disconnected_corridors != True
    with subtests.test("unreachable-key-cells"):
        assert report.unreachable_key_cells != True


def test_generate_perfect(subtests: pytest.Subtests) -> None:
    width = random.randint(7, 20)
    height = random.randint(5, 20)
    config: dict[str, str] = {
        "width": f"{width}",
        "height": f"{height}",
        "entry": "0,0",
        "exit": f"{width - 1},{height - 1}",
        "output_file": "perfect.txt",
        "perfect": "True",
    }
    maze_gen = MazeGenerator(**config)
    maze = maze_gen.generate()
    if not maze:
        raise Exception("Maze did not generate.")
    grid = Grid(
        maze.width,
        maze.height,
        from_file=config["output_file"],
        on_each_char=lambda x: Walls(int(x, 16)),
    )
    print(grid)
    printer = MazePrinter(**config)
    printer.display_maze()
    m = MAZE.from_file(config["output_file"])
    report = analyze(m)
    print(render(report, 2, 2))
    with subtests.test("coherent"):
        assert not report.incoherent
    with subtests.test("no-loops"):
        assert report.loops == 0
    with subtests.test("not-disconnected"):
        assert not report.disconnected_corridors
