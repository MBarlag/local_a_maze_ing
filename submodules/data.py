from dataclasses import dataclass, field

@dataclass
class Cell:
    x: int
    y: int
    neighbours: list['Cell'] = field(repr=False, default_factory=list)

    def __getitem__(self, index):
        return (self.x, self.y)[index]

@dataclass(repr=False)
class Grid(list):
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        super().__init__([[0 for x in range(self.width)] for y in range(self.height)])
    
    def row(self, n):
        for index in range(len(self)):
            yield Cell(n, index, neighbours=self.neighbours(n, index))

    def column(self, n):
        for index in range(len(self)):
            yield self[index][n]

    def neighbours(self, y,  x):
        coords = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        for x, y in coords:
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                continue
            yield self[y][x]

a = Cell(3,5)
