from dataclasses import dataclass, replace
from enum import Enum, auto
import time


class State(Enum):
    UNHOLY = auto()
    NORMAL = auto()
    BLESSED = auto()


@dataclass(frozen=True)
class Artifact:
    name: str
    power: int
    state: State
    healing_power: int = 0  # Only used when state is RADIANT


def bless_artifact(artifact: Artifact) -> Artifact:
    print(f"Playing blessing animation for {artifact.name}...")
    time.sleep(1)  # Simulate expensive animation
    print("...")
    print("Blessing animation complete!")

    if artifact.state not in (State.NORMAL, State.UNHOLY):
        print("Can only bless normal or unholy artifacts")
        return artifact

    # Blessed artifacts get a healing bonus when made radiant
    return replace(artifact, healing_power=artifact.power * 2)


def make_radiant(artifact: Artifact) -> Artifact:
    if artifact.state in (State.BLESSED, State.NORMAL):
        return replace(artifact, healing_power=artifact.power)
    else:
        print("Only normal or Blessed artifacts can be made radiant")
        return artifact


def main():
    print("First shalt thou take out the Holy Pin.")
    unholy_grenade = Artifact(
        name="Holy Hand Grenade of Antioch",
        power=1000,
        state=State.UNHOLY,
    )

    print("Then shalt thou count to three, no more, no less.")
    normal_grenade = bless_artifact(unholy_grenade)

    print(
        "Four shalt thou not count, neither count thou two, excepting that thou then proceed to three. Five is right out."
    )
    blessed_grenade = bless_artifact(normal_grenade)

    print(
        "Once the number three, being the third number, be reached, then lobbest thou thy Holy Hand Grenade of Antioch towards thy foe, who, being naughty in My sight, shall snuff it."
    )

    radiant_grenade = make_radiant(blessed_grenade)

    # This will play the expensive animation but not change the state, useless call we would want to avoid
    bless_artifact(radiant_grenade)


if __name__ == "__main__":
    main()
