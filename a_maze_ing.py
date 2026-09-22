"""
     a_maze_ing.py

    Is responsible for being a dispatcher tower for all of the classes in the program,
    the orchestrator, 

    It will talk with multiple classes and ask them to do their job, 
    without overwhelming each of the class with information that is not needed.        

"""


# from submodules.config import Config
# from submodules.display import MazePrinter

if __name__ == '__main__':
    pass
    # config = config("config.txt").parse_config()
    # # config looks like: {'height': '4', ...}

    # maze_gen = MazeGen(**config)
    # # under the hood it will call the MazeGen constructor method, 
    # # it will look something like this:
    # #   MazeGen(name="maze_name", height="4", color='red') 
    # # it will not care about parameters that are not defined in its class
    # # and will just take what it actually needs

    # maze_printer = MazePrinter(**config)
    # maze_printer.display()
