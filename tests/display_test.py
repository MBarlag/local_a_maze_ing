from submodules.display import MazePrinter

# Run from project root as a module: python3 -m tests.display_test

if __name__ == '__main__':
    config = {"height": "5", "width": "5", "output_file": "hex_maze.txt"}
    printer = MazePrinter(**config)
    hex_maze = printer._parse_hex()
    print(hex_maze)

    for row in hex_maze:
        printer.display_row(row)
