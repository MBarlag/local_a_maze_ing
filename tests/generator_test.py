from copy import copy
from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from submodules.abstract import Vector
from submodules.config import Config
from submodules.generator import MazeGenerator


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


def test_invalid_config_pipeline(config) -> None:
    with pytest.raises((ValueError, TypeError)):
        print(config)
        MazeGenerator(**config)


def test_output_file() -> None:
    config = Config("tests/good_config.txt").parse_config()
    maze_gen = MazeGenerator(**config)
    maze_gen.generate()
    maze_gen.output()


if __name__ == "__main__":
    test_output_file()
