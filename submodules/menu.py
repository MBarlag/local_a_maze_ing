import sys
from enum import Enum

import inquirer

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


def quit_menu() -> None:
    print("\nBye, hope to see you soon!")
    sys.exit(0)


class Action(Enum):
    GENERATE = generate
    TOGGLE_PATH = toggle_path
    ROTATE_COLORS = rotate_colors
    INPUT_SEED = seed
    QUIT = quit_menu


def choose_action() -> Action:
    """Prompt user to choose an action.

    Returns:
        Action: Enum that represents possible actions
    """
    to_choose_action = [
        inquirer.List(
            name="action",
            message="What would you like to do next?",
            choices=[
                ("Generate a new maze.", Action.GENERATE),
                ("Show/Hide the shortest path.", Action.TOGGLE_PATH),
                ("Rotate the wall colors.", Action.ROTATE_COLORS),
                ("Input a seed.", Action.INPUT_SEED),
                ("Quit Emma's Maze.", Action.QUIT),
            ],
        )
    ]

    # Here the chosen action is returned. Main will execute the action.
    choice: Action = inquirer.prompt(
        to_choose_action, raise_keyboard_interrupt=True)
    return choice.get('action', Action.QUIT)

def prompt_loop() -> None:
    """Runs a prompt loop to get next action from the user."""
    print("Welcome to Emma's amazing maze!")
    user = inquirer.text(message='First, please enter your name')
    input(
        f"Nice to meet you, {user}! Press enter to generate your first maze.\n")
    choice = Action.GENERATE
    while choice:
        choice()
        choice = choose_action()
