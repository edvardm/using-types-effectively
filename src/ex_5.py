from typing import Any, TypeGuard, TypedDict


# `TypedDict` makes the expected structure explicit instead of using raw
# `dict[str, <value type, either union or worse, Any>
class MonsterData(TypedDict):
    name: str
    difficulty: int


def is_monster_data(data: Any) -> TypeGuard[MonsterData]:
    match data:
        case {"name": str(), "difficulty": int(), **_rest}:  # See note 1 below
            return True  # See note 2 below
        case _:
            return False


# NOTE 1: This ensures "name" and "difficulty" exist and have the correct types,
# but does NOT check whether all keys are strings.

# NOTE 2: type signature says it returns TypeGuard[MonsterData], even though we only return True or False.
# This is what mypy documentation calls "smart boolean" (https://mypy.readthedocs.io/en/latest/type_narrowing.html#type-guards):
# If result is True, the type checker will automatically narrow the type to MonsterData.
