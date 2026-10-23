import re
from re import Pattern
from typing import Annotated, Any

from pydantic import (
    BeforeValidator,
    PlainValidator,
    StringConstraints,
    TypeAdapter,
)

from submodules.abstract import Vector


def limited_input(
    strip_whitespace: bool | None = None,
    to_upper: bool | None = None,
    to_lower: bool | None = None,
    strict: bool | None = None,
    min_length: int | None = None,
    max_length: int | None = None,
    pattern: str | Pattern[str] | None = None,
    ascii_only: bool | None = None,
) -> BeforeValidator:
    """BeforeValidator constructor for the input str.

    Args:
        strip_whitespace: Whether validation should strip whitespaces.
        to_upper: Whether validation should change input_str to uppercase.
        to_lower: Whether validation should change input_str to lowercase.
        strict: Whether the input string can be only string.
        min_length: Min length of the input string.
        max_length: Max length of the input string.
        pattern: Regular expression pattern to apply on input str.
        ascii_only: Whether input str should be ascii characters only.

    Returns:
        Returns BeforeValidator. Can be used with Annotated[].

    Raises:
        ValueError if any of the limits has been triggered.
    """
    _STR = TypeAdapter(
        Annotated[
            str,
            StringConstraints(
                strip_whitespace,
                to_upper,
                to_lower,
                strict,
                min_length,
                max_length,
                pattern,
                ascii_only,
            ),
        ]
    )

    def _within_limits(value: Any) -> Any:
        if isinstance(value, str):
            value = _STR.validate_python(value)
        return value

    return BeforeValidator(_within_limits)


def allowed_inputs(*args: str, **kwargs: str) -> BeforeValidator:
    """Checks input_str against allowed word list."""
    allowed = [*args]
    allowed.extend(kwargs.values())

    def within_allowed_inputs(value: Any) -> Any:
        if isinstance(value, str) and value not in allowed:
            raise ValueError(
                f"Value cannot be anything but from allowed list: {allowed=}"
            )
        return value

    return BeforeValidator(within_allowed_inputs)


def blocked_inputs(*args: str, **kwargs: str) -> BeforeValidator:
    """Checks input_str against blocklist of words."""
    blocked = [*args]
    blocked.extend(kwargs.values())

    def not_blocked(value: Any) -> Any:
        if isinstance(value, str) and value in blocked:
            raise ValueError(
                f"Value cannot be part of the blocked list: {blocked=}"
            )
        return value

    return BeforeValidator(not_blocked)


def _to_vector_int(value: Any) -> Vector[int]:
    if not isinstance(value, (Vector, tuple, str)):
        raise TypeError("Unsupported type for Vector[int].")
    if isinstance(value, (Vector, tuple)):
        if len(list(value)) != 2:
            raise ValueError("Vector should have strictly two members.")
        y, x = value
        if not (isinstance(y, int) and isinstance(x, int)):
            raise TypeError("Vector members should be of type int.")
        return Vector[int](y, x)
    positive_ints_pattern = re.compile(r"^\s*([0-9]+)\s*,\s*([0-9]+)\s*$")
    if isinstance(value, str):
        if "\n" in value:
            raise ValueError("Vector argument accepts one-line strings only.")
        match: list[Any] = positive_ints_pattern.findall(value)
        if len(match) != 1:
            raise ValueError("Expected exactly one positive int pair: 'y, x'.")
        pair: list[str] = list(match[0])
        if len(pair) != 2:
            raise ValueError("Vector str should be of format: 'y, x'.")
        ints = [int(n) for n in pair]
        y, x = ints
        return Vector[int](y, x)


PositiveInt = Annotated[int, limited_input(pattern=r"^\d+$")]
FileName = Annotated[
    str,
    blocked_inputs(".", ".."),
    StringConstraints(
        min_length=1,
        max_length=255,
        pattern=r'^[^/\\:*?"<>|\x00-\x1f]+$',
        strict=True,
    ),
]

IntVector = Annotated[
    Vector[int],
    PlainValidator(_to_vector_int),
]
Bool = Annotated[bool, allowed_inputs("False", "True")]
