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


# NOTE: In general, I avoid creating variables for things which are used only once; so instead
# of creating the dictionary and then returning an element from it, I just return the element
# directly.
#
# This saves me the trouble of inventing really good names (which is often hard!) and with
# this style I also know immediately that if a variable has a name, it is very likely used
# more than once (with the exception of some constants and loop variables).
