import re
from typing import Annotated, Any

from pydantic import Field
from pydantic.dataclasses import dataclass
from typing_extensions import TypeAliasType

from submodules.enums import Vector

ShortStr = TypeAliasType("ShortStr", Annotated[str, Field(max_length=3)])

Bool = TypeAliasType("Bool", Annotated[str, Field()])


def extract_tuple(value: Any) -> Vector[int]:
    if isinstance(value, str):
        match = re.fullmatch(r"^\s*([+]?[0-9]+)\s*,\s*([-+]?[0-9]+)\s*\)\s*$")
        if match is None:
            raise


@dataclass
class Test:
    # model_config = ConfigDict(revalidate_instances="always")
    entry: tuple[int, int]
