from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar("T")


@dataclass
class SpellBook:
    name: str
    arcane_level: int


@dataclass
class Item:
    name: str
    value: int


class Inventory(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []

    def add(self, item: T) -> None:
        self.items.append(item)

    def get_all(self) -> List[T]:
        return list(self.items)


books = Inventory[SpellBook]()
books.add(SpellBook("Fireball", 10))  # OK

items = Inventory[Item]()
items.add(Item("Health Potion", 50))  # OK

items.add(SpellBook("Ice Lance", 8))  # mypy error
