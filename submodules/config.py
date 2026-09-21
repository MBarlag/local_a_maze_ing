from dataclasses import dataclass
from pydantic import BaseModel, PrivateAttr
import re

@dataclass
class Config:

    _filename: str

    def parse_config(self) -> dict[str, str]:
        result: dict[str, str] = {}
        with open(self._filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                # handling comments
                line = re.sub("(^#.*$)|(#.*$)", "", line)
                line = line.strip()
                if not line:
                    continue
                splitted = line.split("=")
                if len(splitted) != 2:
                    raise Exception               
                key, value = splitted
                result[key] = value
        return result