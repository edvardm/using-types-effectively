from dataclasses import dataclass


@dataclass(frozen=True)
class Spell:
    name: str
    power: int


@dataclass(frozen=True)
class OffensiveSpell(Spell):
    effect: str


@dataclass(frozen=True)
class SupportSpell(Spell):
    duration: int


def cast_spell(spell: Spell) -> None:
    """❌ Unsafe: Mypy does NOT prevent incorrect spell use."""
    match spell:
        case OffensiveSpell(effect=e):
            print(f"Casting offensive spell: {spell.name} ({e})")
        case SupportSpell(duration=d):
            print(f"Casting support spell: {spell.name} (Duration: {d} turns)")


# Example usage:
fireball = OffensiveSpell(name="Fireball", power=10, effect="fire")
heal = SupportSpell(name="Heal", power=5, duration=3)

cast_spell(fireball)  # ✅ Allowed
cast_spell(heal)  # ✅ Allowed

# We can accidentally mix up spells
mixed_spell = OffensiveSpell(
    name="Weird Heal", power=7, effect="heal"
)  # Invalid use of 'effect'
cast_spell(mixed_spell)  # ❌ Mypy does NOT complain!
