from dataclasses import dataclass
from enum import Enum, auto
from typing import overload
import time


class State(Enum):
    UNHOLY = auto()
    NORMAL = auto()
    BLESSED = auto()


@dataclass(frozen=True)
class Artifact:
    name: str


@dataclass(frozen=True)
class PowerMixin:
    power: int
    area_of_effect: int = 5


@dataclass(frozen=True)
class RadiantMixin:
    healing_power: int


@dataclass(frozen=True)
class UnholyArtifact(Artifact, PowerMixin):
    pass


@dataclass(frozen=True)
class NormalArtifact(Artifact, PowerMixin):
    pass


@dataclass(frozen=True)
class BlessedArtifact(Artifact, PowerMixin):
    pass


@dataclass(frozen=True)
class RadiantNormalArtifact(Artifact, PowerMixin, RadiantMixin):
    pass


@dataclass(frozen=True)
class RadiantBlessedArtifact(Artifact, PowerMixin, RadiantMixin):
    pass


ArtifactState = (
    UnholyArtifact
    | NormalArtifact
    | BlessedArtifact
    | RadiantNormalArtifact
    | RadiantBlessedArtifact
)


@overload
def bless_artifact(artifact: UnholyArtifact) -> NormalArtifact: ...


@overload
def bless_artifact(artifact: NormalArtifact) -> BlessedArtifact: ...


@overload
def bless_artifact(artifact: RadiantNormalArtifact) -> RadiantBlessedArtifact: ...


def bless_artifact(
    artifact: UnholyArtifact | NormalArtifact | RadiantNormalArtifact,
) -> NormalArtifact | BlessedArtifact | RadiantBlessedArtifact:
    print(f"Playing blessing animation for {artifact.name}...")
    time.sleep(1)  # Simulate expensive animation
    print("...")
    print("Blessing animation complete!")

    match artifact:
        case UnholyArtifact(name=name, power=power):
            return NormalArtifact(name=name, power=power)
        case NormalArtifact(name=name, power=power):
            return BlessedArtifact(name=name, power=power)
        case RadiantNormalArtifact(name=name, power=power, healing_power=healing):
            return RadiantBlessedArtifact(name=name, power=power, healing_power=healing)


def make_radiant(
    artifact: NormalArtifact | BlessedArtifact,
) -> RadiantNormalArtifact | RadiantBlessedArtifact:
    match artifact:
        case NormalArtifact(name=name, power=power):
            return RadiantNormalArtifact(name=name, power=power, healing_power=power)
        case BlessedArtifact(name=name, power=power):
            return RadiantBlessedArtifact(
                name=name, power=power, healing_power=power * 2
            )


def use_artifact(artifact: ArtifactState) -> None:
    match artifact:
        case UnholyArtifact(name=name, power=power):
            print(f"Using unholy {name} (power: {power})")
        case NormalArtifact(name=name, power=power):
            print(f"Using normal {name} (power: {power})")
        case BlessedArtifact(name=name, power=power):
            print(f"Using blessed {name} (power: {power})")
        case RadiantNormalArtifact(name=name, power=power, healing_power=healing):
            print(f"Using radiant normal {name} (power: {power}, healing: {healing})")
        case RadiantBlessedArtifact(name=name, power=power, healing_power=healing):
            print(f"Using radiant blessed {name} (power: {power}, healing: {healing})")


def main():
    unholy_grenade = UnholyArtifact(name="Holy Hand Grenade of Antioch", power=1000)

    normal_grenade = bless_artifact(unholy_grenade)
    blessed_grenade = bless_artifact(normal_grenade)

    bless_artifact(make_radiant(blessed_grenade))  # already blessed -> error
