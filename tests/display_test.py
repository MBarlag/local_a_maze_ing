from submodules.display import MazePrinter

# Run from project root as a module: python3 -m tests.display_test

if __name__ == '__main__':
    config = {"width": "25", "height": "20", "entry": "0,0", "exit": "19,14",
              "output_file": "hex_maze.txt"}
    printer = MazePrinter(**config)
    printer.display_maze()
