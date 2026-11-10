"""Classes to read a config file and turn it into a dictionary.

Opens a file and converts its lines to key, value pairs.
Keys hold specifications for creating the maze.
"""

import re
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field, NonNegativeInt

from mazegen.safe_types import Bool, FilePath, IntVector


class ConfigParserError(Exception):
    """Exception for when the config file has an invalid line."""


class MazeConfig(BaseModel):
    """Type safe config that uses pydantic validation."""

    width: NonNegativeInt
    height: NonNegativeInt
    entry: IntVector
    exit: IntVector
    perfect: Bool
    output_file: FilePath
    seed: NonNegativeInt | None = Field(None)

    @property
    def as_dict(self) -> dict[str, str]:
        r"""dict\[str, str] representation."""
        result = {k: str(v) for k, v in vars(self).items()}
        result["entry"] = result["entry"].strip("()")
        result["exit"] = result["exit"].strip("()")
        return result

    @property
    def as_kwargs(self) -> dict[str, Any]:
        r"""\dict[str, Any] representation."""
        return vars(self)


@dataclass
class ConfigParser:
    """Parses lines of a config file.

    Specifications and values are stored as strings.

    Attributes:
        filename: Path to the config file.
    """

    filename: str

    @staticmethod
    def _strip_comments(line: str) -> str:
        """Removes comments anywhere on the line."""
        return re.sub(pattern="(#.*$)", repl="", string=line)

    @staticmethod
    def _extract_pair(line: str) -> tuple[str, str] | None:
        """Splits a line into a tuple of name and value."""
        if not line:
            return None
        split_result = line.split("=")
        if len(split_result) != 2:
            message = "There can only be one = sign per config line."
            raise ConfigParserError(message)
        name, value = split_result
        return name, value

    def parse(self) -> dict[str, Any]:
        r"""Parse config to dict\[str, str]."""
        result: dict[str, str] = {}
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                line = self._strip_comments(line).strip()
                if not (extracted := self._extract_pair(line)):
                    continue
                key, value = extracted
                k = key.lower().strip()
                result[k] = value.strip()
        return result
