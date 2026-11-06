##!/usr/bin/env python3
"""a_maze_ing.py.

Is responsible for being a dispatcher tower
for all of the classes in the program, the orchestrator,

It will talk with multiple classes and ask them to do their job,
without overwhelming each of the class with information that is not needed.

"""

import sys
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

from pydantic import ValidationError

from submodules.config import ConfigParser
from submodules.display import MazePrinter
from submodules.generator import MazeGenerator
from submodules.menu import Menu


@contextmanager
def graceful_errors(
    skip_on_interrupt: bool = True,
) -> Generator[Any]:
    """Handles errors gracefully, skips on KeyboardInterrupt by default."""
    try:
        # After yield is called, it's gonna
        # basically resume execution from here
        # of everything within the with graceful_errors() block
        # if it raises an Exception, it will be caught by the try except
        yield
    except (KeyboardInterrupt, Exception) as e:
        if isinstance(e, KeyboardInterrupt):
            if skip_on_interrupt:
                # when we return it jumps to next line outside the with
                return
            else:
                raise
        handle_critical_error(e)


def format_pydantic_error(e: ValidationError) -> str:
    """Formats pydantic error."""
    root = "[A-Maze-ing]"
    result = root
    result += f"[{e.title} x{e.error_count()} validation error(s)]:\n"
    for error in e.errors(include_url=False):
        # loc is a tuple of int | str
        # int if it's an index of the value in question
        # str if its an attribute
        # "".join(...) means concatenate all of the items within
        attr_name = "".join(
            f".{x}" if isinstance(x, str) else f"[{x}]" for x in error["loc"]
        ).strip(".")
        # exc_name = error["type"].title().replace("_", "")
        result += f"    {attr_name} ({error['input']!r}) <-- {error['msg']}\n"
    return result[:-1]


def handle_critical_error(e: Exception) -> None:
    """Displays an error and exits gracefully."""
    root = "[A-Maze-ing]"
    if isinstance(e, ValidationError):
        print(format_pydantic_error(e), file=sys.stderr)
    else:
        exc_name = type(e).__name__
        print(f"{root}[{exc_name}]: {e!s}", file=sys.stderr)
    sys.exit(1)


class AMazeIngError(Exception):
    """Error related to the workings of AMazeIng."""


if __name__ == "__main__":
    with graceful_errors():
        if len(sys.argv) != 2:
            raise AMazeIngError("Usage: python3 a_maze_ing.py <file>")
        config = ConfigParser(sys.argv[1]).parse()
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
