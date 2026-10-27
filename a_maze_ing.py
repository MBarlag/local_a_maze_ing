#!/usr/bin/env python3
"""a_maze_ing.py.

Is responsible for being a dispatcher tower
for all of the classes in the program, the orchestrator,

It will talk with multiple classes and ask them to do their job,
without overwhelming each of the class with information that is not needed.

"""

import sys

from submodules.config import Config
from submodules.display import MazePrinter
from mazegen.generator import MazeGenerator
from submodules.menu import Menu


def handle_critical_error(e: Exception) -> None:
    """Displayes an error and exits gracefully."""
    exc_name = type(e).__name__
    print(f"[A-Maze-ing][{exc_name}]: {e!s}")
    sys.exit(1)

class AMazeIngError(Exception):
    """Error related to the workings of AMazeIng."""

if __name__ == "__main__":
    try:
        # if len(sys.argv) != 2:
        #     raise AttributeError("Usage: python3 a_maze_ing.py <file>")
        config_filename = "config.txt"
        config = Config(config_filename).parse_config()
        # Don't forget to use sys.argv[1] here instead of config.txt!
        maze_gen = MazeGenerator(**config)
        # under the hood it will call the MazeGen constructor method,
        # it will look something like this:
        #   MazeGen(name="maze_name", height="4", color='red')
        # it will not care about parameters that are not defined in its class
        # and will just take what it actually needs

        maze_printer = MazePrinter(**config)
    except Exception as e:
        handle_critical_error(e)
    menu = Menu(maze_gen, maze_printer)
    try:
        menu.prompt_loop()
    except (KeyboardInterrupt, Exception) as e:
        if isinstance(e, KeyboardInterrupt):
            menu.quit_menu()
        else:
            handle_critical_error(e)
