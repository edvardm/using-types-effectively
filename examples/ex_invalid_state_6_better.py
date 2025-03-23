from dataclasses import dataclass
from typing import overload, TypeVar
import time


@dataclass(frozen=True, kw_only=True)
class BaseArtifact:
    name: str
    power: int


@dataclass(frozen=True)
class UnholyArtifact(BaseArtifact): ...


@dataclass(frozen=True)
class NormalArtifact(BaseArtifact): ...


@dataclass(frozen=True)
class BlessedArtifact(BaseArtifact): ...


@dataclass(frozen=True)
class RadiantArtifact(BaseArtifact):
    healing_power: int


@dataclass(frozen=True)
class RadiantBlessedArtifact(BaseArtifact):
    healing_power: int


T = TypeVar("T", UnholyArtifact, NormalArtifact, RadiantArtifact)


@overload
def bless_artifact(artifact: UnholyArtifact) -> NormalArtifact: ...
@overload
def bless_artifact(artifact: NormalArtifact) -> BlessedArtifact: ...
@overload
def bless_artifact(artifact: RadiantArtifact) -> RadiantBlessedArtifact: ...


def bless_artifact(
    artifact: T,
) -> NormalArtifact | BlessedArtifact | RadiantBlessedArtifact:
    print(f"Playing blessing animation for {artifact.name}...")
    time.sleep(1)  # Simulate expensive animation
    print("... Blessing animation complete!")

    if isinstance(artifact, UnholyArtifact):
        return NormalArtifact(name=artifact.name, power=artifact.power)
    elif isinstance(artifact, NormalArtifact):
        return BlessedArtifact(name=artifact.name, power=artifact.power)
    elif isinstance(artifact, RadiantArtifact):
        return RadiantBlessedArtifact(
            name=artifact.name,
            power=artifact.power,
            healing_power=artifact.healing_power,
        )
    else:
        raise ValueError("Invalid artifact for blessing")


U = TypeVar("U", NormalArtifact, BlessedArtifact)


@overload
def make_radiant(artifact: NormalArtifact) -> RadiantArtifact: ...
@overload
def make_radiant(artifact: BlessedArtifact) -> RadiantBlessedArtifact: ...


def make_radiant(artifact: U) -> RadiantArtifact | RadiantBlessedArtifact:
    match artifact:
        case NormalArtifact():
            return RadiantArtifact(
                name=artifact.name, power=artifact.power, healing_power=artifact.power
            )
        case BlessedArtifact():
            return RadiantBlessedArtifact(
                name=artifact.name,
                power=artifact.power,
                healing_power=artifact.power * 2,
            )


unholy_grenade = UnholyArtifact(name="(Not so) Holy Hand Grenade of Antioch", power=1024)

# must fail to type-check
make_radiant(unholy_grenade)  # type: ignore

normal_grenade = bless_artifact(unholy_grenade)
blessed_grenade = bless_artifact(normal_grenade)

make_radiant(normal_grenade)
make_radiant(blessed_grenade)

# must fail to type-check
bless_artifact(blessed_grenade)  # type: ignore
