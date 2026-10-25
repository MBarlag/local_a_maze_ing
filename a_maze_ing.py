#!/bin/python
"""a_maze_ing.py.

Is responsible for being a dispatcher tower
for all of the classes in the program, the orchestrator,

It will talk with multiple classes and ask them to do their job,
without overwhelming each of the class with information that is not needed.

"""
import sys

from submodules.generator import MazeGenerator
from submodules.menu import Menu, quit_menu
from submodules.config import Config, ConfigException
from submodules.display import MazePrinter

if __name__ == "__main__":
    # if len(sys.argv) not 2:
    #   raise Exception ("Usage: python3 a_maze_ing.py <file>")

    try:
        config = Config("config.txt").parse_config()
        # Don't forget to use sys.argv[1] here instead of config.txt!
        maze_gen = MazeGenerator(**config)
        # under the hood it will call the MazeGen constructor method,
        # it will look something like this:
        #   MazeGen(name="maze_name", height="4", color='red')
        # it will not care about parameters that are not defined in its class
        # and will just take what it actually needs

        maze_printer = MazePrinter(**config)
    except:
        print()

    menu = Menu(maze_gen, maze_printer)
    try:
        menu.prompt_loop()
    except (KeyboardInterrupt, Exception) as error:
        if isinstance(error, KeyboardInterrupt):
            menu.quit_menu()
        else:
            print(f"Program ran into an error: \n{error=}")
