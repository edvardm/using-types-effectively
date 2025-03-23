from typing import TypeVar, Generic, Callable
from dataclasses import dataclass
import re

T = TypeVar("T")
Marker = TypeVar("Marker")


@dataclass
class Phantom(Generic[T, Marker]):
    v: T


# fmt: off
class Safe: ...  # actual phantom type
class SafetyCheckError(Exception): ...
# fmt: on


def validate(value: T, pred: Callable[[T], bool]) -> Phantom[T, Safe]:
    if pred(value):
        return Phantom(value)

    raise SafetyCheckError(f"Validation failed for value: {value!r}")


def read_scroll(scroll: Phantom[str, Safe]) -> None:
    print(f"Reading scroll {scroll.v}")


def main() -> None:
    unchecked_scroll = "enchant weapon'; DROP TABLE INVENTORY; --"

    try:
        safe_scroll = validate(
            unchecked_scroll.strip(), lambda s: bool(re.match(r"^[a-z ]$", s))
        )
        read_scroll(safe_scroll)  # ok
    except SafetyCheckError as e:
        print(f"Error: {e}")

    # fails to typecheck as desired
    read_scroll(unchecked_scroll)  # type: ignore[arg-type]
