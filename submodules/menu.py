"""An interactive menu which prompts actions to the user.

Enums are used to give each menu option a name. The user sees a list
of possible actions and uses the arrow and enter keys to choose an action.
After excecuting, main will lead the user back to the menu until they
choose to quit the program.
"""

import sys
import inquirer
from enum import Enum
from typing import Any

from submodules.display import MazePrinter, COLOR_1, COLOR_2
from submodules.generator import MazeGenerator, MazeGenException


class Action(Enum):
    """Enum for actions."""

    GENERATE = 1
    TOGGLE_PATH = 2
    CHANGE_COLORS = 3
    INPUT_SEED = 4
    QUIT = 5


class Menu:
    """Interactive menu to get input and dispatch actions."""

    def __init__(
        self, maze_gen: MazeGenerator, maze_printer: MazePrinter
    ) -> None:
        self.maze_gen = maze_gen
        self.maze_printer = maze_printer

    def prompt_loop(self) -> None:
        """Runs a prompt loop to get next action from the user."""
        print("Welcome to Emma's amazing maze!")
        user = inquirer.text(message="First, please enter your name")
        input(
            f"Nice to meet you, {user}! "
            "Press enter to generate your first maze.\n"
        )
        choice = Action.GENERATE
        while choice:
            self.execute(choice)
            choice = choose_action()

    def generate(self) -> None:
        """Generates a maze and prints it in the terminal."""
        try:
            self.maze_gen.generate()
        except MazeGenException as error:
            print(f"Could not generate a new maze: {error}.")
            return
        self.maze_printer.display_maze()

    def toggle_path(self) -> None:
        """Activates or deactivates path visibility and redraws maze."""
        self.maze_printer.path_visible = not self.maze_printer.path_visible
        self.maze_printer.display_maze()

    def change_colors(self) -> None:
        """Changes the colors of the walls in current maze."""
        if self.maze_printer.wall_color == COLOR_1:
            self.maze_printer.wall_color = COLOR_2
        elif self.maze_printer.wall_color == COLOR_2:
            self.maze_printer.wall_color = COLOR_1
        self.maze_printer.display_maze()

    def seed(self) -> None:
        """Ask user input to change the seed."""
        print(f"Current seed is {self.maze_gen.seed}.")
        while True:
            print("Please type a positive int to change the seed:")
            try:
                user_seed = int(input())
            except ValueError:
                print("Input is not an int, please try again.")
                continue    
            if user_seed < 0:
                print("Input is invalid, please try again.")
                continue
            break
        self.maze_gen.seed = user_seed
        print(f"Seed is now {self.maze_gen.seed}.\n")

    def execute(self, n: Action) -> None:
        "Receive action parameter and dispatch to the correct method."
        match n:
            case Action.GENERATE:
                self.generate()
            case Action.TOGGLE_PATH:
                self.toggle_path()
            case Action.CHANGE_COLORS:
                self.change_colors()
            case Action.INPUT_SEED:
                self.seed()
            case Action.QUIT:
                self.quit_menu()

    def quit_menu(self) -> None:
        print("\nBye, hope to see you soon!")
        sys.exit(0)


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
                ("Change the wall colors.", Action.CHANGE_COLORS),
                ("Get current seed and input a seed.", Action.INPUT_SEED),
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
