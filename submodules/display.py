from pydantic import BaseModel

class MazePrinter(BaseModel):
    def __init__(self, width: int, height: int, **kwargs: Any) -> None:
        self.width = int(width)
        self.height = int(height)