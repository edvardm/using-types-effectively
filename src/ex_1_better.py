from enum import Enum


class WeaponType(Enum):
    SWORD = "sword"
    BOW = "bow"
    STAFF = "staff"


class AttackType(Enum):
    QUICK = "quick"
    STRONG = "strong"
    SPECIAL = "special"


def attack_enemy(weapon: WeaponType, attack_type: AttackType) -> int | None:
    return {
        WeaponType.SWORD: {
            AttackType.QUICK: 5,
            AttackType.STRONG: 10,
            AttackType.SPECIAL: 15,
        },
        WeaponType.BOW: {
            AttackType.QUICK: 3,
            AttackType.STRONG: 7,
            AttackType.SPECIAL: 12,
        },
        WeaponType.STAFF: {
            AttackType.QUICK: 2,
            AttackType.STRONG: 4,
            AttackType.SPECIAL: 20,
        },
    }[weapon][attack_type]
