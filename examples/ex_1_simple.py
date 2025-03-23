def attack_enemy(weapon: str, attack_type: str) -> int:
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
