from dataclasses import dataclass

def error() -> None:
    print("Error")

@dataclass
class Config:

    _filename: str

    def parse_config(self) -> dict[str, str]:
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
