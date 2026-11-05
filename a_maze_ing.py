#!/usr/bin/env python3
"""a_maze_ing.py.

Is responsible for being a dispatcher tower
for all of the classes in the program, the orchestrator,

It will talk with multiple classes and ask them to do their job,
without overwhelming each of the class with information that is not needed.

"""

import sys
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from pydantic import ValidationError

from submodules.config import Config
from submodules.display import MazePrinter
from submodules.generator import MazeGenerator
from submodules.menu import Menu


@contextmanager
def graceful_errors(
    skip_on_interrupt: bool = True,
) -> Iterator[Any]:
    """Handles errors gracefully, skips on KeyboardInterrupt by default."""
    try:
        yield
    except (KeyboardInterrupt, Exception) as e:
        if isinstance(e, KeyboardInterrupt):
            if skip_on_interrupt:
                return
            else:
                raise
        handle_critical_error(e)


def handle_critical_error(e: Exception) -> None:
    """Displays an error and exits gracefully."""
    root = "[A-Maze-ing]"
    if isinstance(e, ValidationError):
        print(f"{root}[{e.title} x{e.error_count()}]:", file=sys.stderr)
        for error in e.errors(include_url=False):
            loc = "".join(
                f".{x}" if isinstance(x, str) else f"[{x}]"
                for x in error["loc"]
            ).strip(".")
            exc_name = error["type"].title().replace("_", "")
            print(
                f"    {loc}={error['input']!r} <-- {error['msg']}",
                file=sys.stderr,
            )
    else:
        exc_name = type(e).__name__
        print(f"{root}[{exc_name}]: {e!s}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    with graceful_errors():
        if len(sys.argv) != 2:
            raise Exception("Usage: python3 a_maze_ing.py <file>")
        config = Config(sys.argv[1]).parse_config()
        # Don't forget to use sys.argv[1] here instead of config.txt!
        maze_gen = MazeGenerator(**config)
        # under the hood it will call the MazeGen constructor method,
        # it will look something like this:
        #   MazeGen(name="maze_name", height="4", color='red')
        # it will not care about parameters that are not defined in its class
        # and will just take what it actually needs

        maze_printer = MazePrinter(**config)
        menu = Menu(maze_gen, maze_printer)
        menu.prompt_loop()
    menu.quit_menu()
