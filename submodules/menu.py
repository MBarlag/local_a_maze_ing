import sys
import inquirer
from enum import Enum # Not needed when moving the enum Class to enums.py.


class Option(Enum):
    NEW_MAZE = 1
    PATH = 2
    ROTATE_COLOURS = 3
    INPUT_SEED = 4
    QUIT = 5


def input_option() -> Option:
    option_prompt = [
        inquirer.List(
            "option",
            message="What would you like to do next?",
            choices=[
                ("Generate a new maze.", Option.NEW_MAZE),
                ("Show/Hide the shortest path.", Option.PATH),
                ("Rotate the wall colours.", Option.ROTATE_COLOURS),
                ("Input a seed.", Option.INPUT_SEED),
                ("Quit Emma's Maze.", Option.QUIT),
            ],
        )
    ]
    choice: Option = inquirer.prompt(option_prompt)
    return(choice) #Here the chosen option is returned. Main will execute the action.


def start() -> None: # I think we should move this part, or a part like this, to main?
    print("Welcome to Emma's amazing maze!")
    user = inquirer.text(message='First, please enter your name')
    try:
        input(f"Nice to meet you, {user}! Press enter to generate your first maze.\n")
    except KeyboardInterrupt:
        print("\nBye, hope to see you soon!")
        sys.exit(0) # exiting the program also has to happen in main?


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

    choice = input_option() # This is where we move from main to menu.py?


if __name__ == '__main__':
    start()


    # option_prompt = [
    #     inquirer.List('topics', message='What would you like to do next?', choices=['new maze', 'path'], ),
    #     inquirer.Confirm('confirm',  message='Do you want to continue?', default=False),
    # ]

    # answers = inquirer.prompt(options)
    # print(answers)
