"""
     a_maze_ing.py

    Is responsible for being a dispatcher tower for all of the classes in the program,
    the orchestrator, 

    It will talk with multiple classes and ask them to do their job, 
    without overwhelming each of the class with information that is not needed.        

"""

import sys
import inquirer
from enum import Enum # Not needed when moving the enum Class to enums.py.

# placeholder for actions
def generate():
    print("generating")
    print("///// [This is a representation of a possible Maze] /////\n")
    print("+------------------------------+\n"
    "|                              |\n"
    "|                              |\n"
    "|                              |\n"
    "|                              |\n"
    "|                              |\n"
    "|                              |\n"
    "|                              |\n"
    "|                              |\n"
    "+------------------------------+\n")
def toggle_path() -> None:
    print("toggle path")
def rotate_colors() -> None:
    print("rotate")
def seed() -> None:
    print("seed")
def quit() -> None:
    print("\nBye, hope to see you soon!")
    sys.exit(0)


class Action(Enum):
    GENERATE = generate
    TOGGLE_PATH = toggle_path
    ROTATE_COLORS = rotate_colors
    INPUT_SEED = seed
    QUIT = quit


def choose_action() -> Action:
    to_choose_action = [
        inquirer.List(
            name="action",
            message="What would you like to do next?",
            choices=[
                ("Generate a new maze.", Action.GENERATE),
                ("Show/Hide the shortest path.", Action.TOGGLE_PATH),
                ("Rotate the wall colours.", Action.ROTATE_COLORS),
                ("Input a seed.", Action.INPUT_SEED),
                ("Quit Emma's Maze.", Action.QUIT),
            ],
        )
    ]

    #Here the chosen action is returned. Main will execute the action.
    choice: Action = inquirer.prompt(to_choose_action, raise_keyboard_interrupt=True)
    return choice.get('action', Action.QUIT)

def prompt_loop() -> None: # I think we should move this part, or a part like this, to main?
    print("Welcome to Emma's amazing maze!")
    user = inquirer.text(message='First, please enter your name')
    input(f"Nice to meet you, {user}! Press enter to generate your first maze.\n")
    choice = Action.GENERATE
    while choice:
        choice()
        choice = choose_action() # This is where we move from main to menu.py?
    # option_prompt = [
    #     inquirer.List('topics', message='What would you like to do next?', choices=['new maze', 'path'], ),
    #     inquirer.Confirm('confirm',  message='Do you want to continue?', default=False),
    # ]

    # answers = inquirer.prompt(options)
    # print(answers)


# from submodules.config import Config
# from submodules.display import MazePrinter

if __name__ == '__main__':

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
    try:
        prompt_loop()
    except (BaseException, Exception) as error:
        if isinstance(error, KeyboardInterrupt):
            quit()
        elif not isinstance(error, SystemExit):
            print(f"Program run into an error: \n{error=}")
