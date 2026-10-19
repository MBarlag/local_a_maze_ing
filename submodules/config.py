"""Classes to read a config file and turn it into a dictionary.

Opens a file and converts its lines to key, value pairs.
Keys hold specifications for creating the maze.
"""

import re
from dataclasses import dataclass
from typing import Any


class ConfigException(Exception):
    """Exception for when the config file has an invalid line."""


@dataclass
class Config:
    """Parses lines of a config file into a dictionary.

    Specifications and values are stored as strings.

    Attributes:
        _filename: Path to the config file.
    """

    _filename: str

    @staticmethod
    def _strip_comments(line: str) -> str:
        """Removes comments anywhere on the line."""
        return re.sub(pattern="(#.*$)", repl="", string=line)

    @staticmethod
    def _extract_pair(line: str, default: Any = None) -> tuple[str, str]:
        """Splits a line into a tuple of specification and value.

        Args:
            line (str): A stripped line from the file.
            default (Any, optional): Defaults to None
            and is returned when line is empty.

        Returns:
            tuple[str, str]: Extracted pair of key and value.

        Raises:
            ConfigException: If the line doen't contain one '='.
        """
        if not line:
            return default
        split_result = line.split("=")
        if (len(split_result) != 2):
            message = "There can only be one = sign per onfig the line"
            raise ConfigException(message)
        return split_result[0], split_result[1]

    def parse_config(self) -> dict[str, str]:
        """Opens file and parses the lines using private methods.

        Returns:
            dict[str, str]: Holds specifications for creating the maze.
        """
        result: dict[str, str] = {}
        with open(self._filename, "r", encoding="utf-8") as f:
            for line in f:
                line = Config._strip_comments(line).strip()
                if not (extracted := Config._extract_pair(line)):
                    continue
                extracted = Config._extract_pair(line)
                key, value = extracted
                result[key.lower()] = value
        return result
