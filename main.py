from pydantic import BaseModel
import platform

def error() -> None:
	print("Error")

class Config(BaseModel):

	def set_height(self, height: int) -> None:
		pass

	def read_config(cls) -> 'Config':
		if cls.instance == None:
			cls.instance = cls(height, width, something, ...)
		return cls.instance

	def __init__(self, filename) -> None:
		# we are reading from file
		with open(filename, "r", encoding="utf-8") as f:
			lines = f.readlines()
			for line in lines:
				# handling comments
				if line.strip()[0] == '#':
					continue
				splitted = line.split("=")
				if len(splitted) != 2:
					error()
					return
				setattr(self, splitted[0], splitted[1])
				
			# self.width = 3
			# self.something = True
			# self.build_realted = 3
			# self.display_related = 3

if __name__ == '__main__':
	config = Config.read_config()
	maze_build(Config)
	print_maze(Config)