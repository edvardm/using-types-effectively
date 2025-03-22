from dataclasses import dataclass


@dataclass
class Potion:
    name: str
    healing: int


@dataclass
class Scroll:
    name: str
    spell: str


@dataclass
class Weapon:
    name: str
    damage: int


Item = Potion | Scroll | Weapon


def use_item(item: Item) -> str:
    match item:
        case Potion(name=name, healing=healing):
            return f"Grabbed healing potion {name}, heals {healing} HP"
        case Scroll(name=name, spell=spell):
            return f"Grabbed scroll of {spell} ({name})"
        case Weapon(name=name, damage=damage):
            return f"Grabbed {name}, dealing {damage} damage)"
