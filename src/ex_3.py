from typing import NewType

MonsterID = NewType("MonsterID", int)
PlayerID = NewType("PlayerID", int)


def damage_monster(monster_id: MonsterID, amount: int) -> int:
    print(f"Damaging monster {monster_id} by {amount}")
    return amount


def heal_player(player_id: PlayerID, amount: int) -> None:
    print(f"Healing player {player_id} by {amount}")


monster_id = MonsterID(42)
player_id = PlayerID(1)

damage_monster(monster_id, 10)  # OK
heal_player(player_id, 5)  # OK

damage_monster(player_id, 10)
