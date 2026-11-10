from typing import Any

from mazegen import MazeGenerator
from mazegen.abstract import Vector

from display import MazePrinter

dict_config: dict[str, Any] = {
    "width": "10",
    "height": "12",
    "output_file": "imperfect.txt",
    "perfect": "False",
    "exit": "9,11",
}
maze_gen = MazeGenerator(entry=Vector(3, 0), **dict_config)
maze = maze_gen.generate()
print(maze.view(lambda r: str(r.walls)))
with open("imperfect.txt", "r", encoding="utf-8") as f:
    print(f.read())
print(f"Path: {maze_gen.path}")
dict_config["entry"] = "3,0"
printer = MazePrinter(path_visible=True, **dict_config)
printer.display_maze()
