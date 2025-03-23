from typing import Literal


def attack_enemy(
    weapon: Literal["sword", "bow", "staff"],
    attack_type: Literal["quick", "strong", "special"],
) -> int:
    return {
        "sword": {
            "quick": 5,
            "strong": 10,
            "special": 15,
        },
        "bow": {"quick": 3, "strong": 7, "special": 12},
        "staff": {
            "quick": 2,
            "strong": 4,
            "special": 20,
        },
    }[weapon][attack_type]
