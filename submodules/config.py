from dataclasses import dataclass
from pydantic import BaseModel, PrivateAttr
from typing import Any
import re

@dataclass
class Config:

    _filename: str

    @staticmethod
    def _strip_comments(line: str) -> str:
        return re.sub(pattern="(#.*$)", repl="", string=line)

    @staticmethod
    def _extract(line: str, default: Any = None) -> bool:
        if not line:
            return default
        split_result = line.split("=")
        if (len(split_result) != 2):
            raise Exception
        return split_result
    
    def parse_config(self) -> dict[str, str]:
        result: dict[str, str] = {}
        with open(self._filename, "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = Config._strip_comments(line).strip()
                if not (extracted := Config._extract(line)):
                    continue
                key, value = extracted
                result[key.lower()] = value
        return result
