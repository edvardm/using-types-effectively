from typing import Any, TypeGuard, TypedDict


class MonsterData(TypedDict):  # <1>
    name: str
    difficulty: int


def is_monster_data(data: Any) -> TypeGuard[MonsterData]:
    match data:
        case {"name": str(), "difficulty": int(), **_rest}:  # <2>
            return True  # <3>
        case _:
            return False
