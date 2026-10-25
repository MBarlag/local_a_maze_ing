"""An interactive menu which prompts actions to the user.

Enums are used to give each menu option a name. The user sees a list
of possible actions and uses the arrow and enter keys to choose an action.
After excecuting, main will lead the user back to the menu until they
choose to quit the program.
"""

import sys
from enum import Enum
from typing import Any

import inquirer

from submodules.display import MazePrinter

# placeholder for actions


def generate() -> None:
    # configurator = Config("config.txt")
    # config = configurator.parse_config()

    print("generating")
    print("///// [This is a representation of a possible Maze] /////\n")
    print(
        "+------------------------------+\n"
        "|                              |\n"
        "|                              |\n"
        "|                              |\n"
        "|                              |\n"
        "|                              |\n"
        "|                              |\n"
        "|                              |\n"
        "|                              |\n"
        "+------------------------------+\n"
    )


def toggle_path(printer: MazePrinter) -> None:
    """Activates or deactivates path visibility and redraws maze."""
    printer.path_visible = not printer.path_visible
    printer.display_maze()
    print("toggle path")


def rotate_colors() -> None:
    print("rotate")


def seed() -> None:
    print("seed")


def quit_menu() -> None:
    print("\nBye, hope to see you soon!")
    sys.exit(0)


class Action(Enum):
    GENERATE = 1
    TOGGLE_PATH = 2
    ROTATE_COLORS = 3
    INPUT_SEED = 4
    QUIT = 5


def execute(n: Action) -> None:
    match n:
        case Action.GENERATE:
            generate()
        case Action.TOGGLE_PATH:
            toggle_path()
        case Action.ROTATE_COLORS:
            rotate_colors()
        case Action.INPUT_SEED:
            seed()
        case Action.QUIT:
            quit_menu()


def choose_action() -> Action:
    """Prompt user to choose an action.

    Returns:
        Action: Enum that represents possible actions.
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

    choice: dict[str, Any] = inquirer.prompt(
        to_choose_action, raise_keyboard_interrupt=True
    )
    answer = choice.get("action", Action.QUIT)
    if isinstance(answer, Action):
        return answer
    return Action.QUIT


def prompt_loop() -> None:
    """Runs a prompt loop to get next action from the user."""
    print("Welcome to Emma's amazing maze!")
    user = inquirer.text(message="First, please enter your name")
    input(
        f"Nice to meet you, {user}! Press enter to generate your first maze.\n"
    )
    choice = Action.GENERATE
    while choice:
        execute(choice)
        choice = choose_action()
