from dataclasses import dataclass, replace
from typing import NewType, TypeVar, Generic, overload, Any
import time

Unholy = NewType("Unholy", object)
Normal = NewType("Normal", object)
Blessed = NewType("Blessed", object)

T = TypeVar("T", Unholy, Normal, Blessed)


@dataclass(frozen=True)
class BaseArtifact(Generic[T]):
    name: str
    power: int


@dataclass(frozen=True)
class Artifact(BaseArtifact[T]): ...


@dataclass(frozen=True)
class RadiantArtifact(BaseArtifact[T]):
    healing_power: int = 0


ArtifactType = Artifact[T] | RadiantArtifact[T]


@overload
def bless_artifact(artifact: Artifact[Unholy]) -> Artifact[Normal]: ...
@overload
def bless_artifact(artifact: Artifact[Normal]) -> Artifact[Blessed]: ...
@overload
def bless_artifact(
    artifact: RadiantArtifact[Normal],
) -> RadiantArtifact[Blessed]: ...  # <1>


def bless_artifact(artifact: ArtifactType[T]) -> ArtifactType:  # type: ignore[type-arg] # <2>
    print(f"Playing blessing animation for {artifact.name}...")
    time.sleep(1)
    print("...")
    print("Blessing animation complete!")

    return replace(artifact)


@overload
def make_radiant(artifact: Artifact[Normal]) -> RadiantArtifact[Normal]: ...


@overload
def make_radiant(artifact: Artifact[Blessed]) -> RadiantArtifact[Blessed]: ...


def make_radiant(artifact: Any) -> Any:
    return RadiantArtifact(
        name=artifact.name, power=artifact.power, healing_power=artifact.power
    )


@overload
def use_artifact(artifact: Artifact[Unholy]) -> None: ...
@overload
def use_artifact(artifact: Artifact[Normal]) -> None: ...
@overload
def use_artifact(artifact: Artifact[Blessed]) -> None: ...
@overload
def use_artifact(artifact: RadiantArtifact[Normal]) -> None: ...
@overload
def use_artifact(artifact: RadiantArtifact[Blessed]) -> None: ...


def use_artifact(artifact: ArtifactType[Any]) -> None:
    match artifact:  # <1>
        case RadiantArtifact(name=name, power=power, healing_power=healing):
            print(f"Using radiant artifact {name=} (power={power}, healing={healing})")
        case Artifact(name=name, power=power):
            print(f"Using standard artifact {name=} (power={power})")


unholy_grenade = Artifact[Unholy](  # for some reason it was unholy when we found it..
    name="(Not so) Holy Hand Grenade of Antioch",
    power=1024,
)

normal_grenade = bless_artifact(unholy_grenade)
blessed_grenade = bless_artifact(normal_grenade)

# must fail to type check
blessed_grenade = bless_artifact(blessed_grenade)  # type: ignore

radiant_normal = make_radiant(normal_grenade)
radiant_blessed = make_radiant(blessed_grenade)

# must fail to type check
make_radiant(unholy_grenade)  # type: ignore

use_artifact(unholy_grenade)
use_artifact(normal_grenade)
use_artifact(blessed_grenade)
use_artifact(radiant_normal)
use_artifact(radiant_blessed)
