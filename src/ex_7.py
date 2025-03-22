from dataclasses import dataclass
from typing import NewType, TypeVar, Generic, overload
import time

# Phantom types
Unholy = NewType("Unholy", None)
Normal = NewType("Normal", None)
Blessed = NewType("Blessed", None)

Radiant = NewType("Radiant", None)
# End of phantom types

T = TypeVar("T", Unholy, Normal, Blessed)
R = TypeVar("R", Radiant, None)


@dataclass(frozen=True)
class Artifact(Generic[T, R]):
    name: str
    power: int
    healing_power: int = 0  # Only used when R is Radiant


@overload
def bless_artifact(artifact: Artifact[Unholy, None]) -> Artifact[Normal, None]: ...


@overload
def bless_artifact(artifact: Artifact[Normal, None]) -> Artifact[Blessed, None]: ...


@overload
def bless_artifact(
    artifact: Artifact[Normal, Radiant],
) -> Artifact[Blessed, Radiant]: ...


def bless_artifact(
    artifact: Artifact[Unholy, R] | Artifact[Normal, R] | Artifact[Normal, Radiant],
) -> Artifact[Normal, R] | Artifact[Blessed, R] | Artifact[Blessed, Radiant]:
    print(f"Playing blessing animation for {artifact.name}...")
    time.sleep(1)
    print("...")
    print("Blessing animation complete!")

    return Artifact(
        name=artifact.name,
        power=artifact.power,
        healing_power=artifact.healing_power,
    )


@overload
def make_radiant(artifact: Artifact[Normal, None]) -> Artifact[Normal, Radiant]: ...


@overload
def make_radiant(artifact: Artifact[Blessed, None]) -> Artifact[Blessed, Radiant]: ...


def make_radiant(
    artifact: Artifact[Normal, None] | Artifact[Blessed, None],
) -> Artifact[Normal, Radiant] | Artifact[Blessed, Radiant]:
    return Artifact(
        name=artifact.name,
        power=artifact.power,
        healing_power=artifact.power,  # Type system ensures this is valid call
    )


@overload
def use_artifact(artifact: Artifact[Unholy, None]) -> None: ...


@overload
def use_artifact(artifact: Artifact[Normal, None]) -> None: ...


@overload
def use_artifact(artifact: Artifact[Blessed, None]) -> None: ...


@overload
def use_artifact(artifact: Artifact[Normal, Radiant]) -> None: ...


@overload
def use_artifact(artifact: Artifact[Blessed, Radiant]) -> None: ...


def use_artifact(artifact: Artifact[T, R]) -> None:
    print(
        f"Using{artifact.name} (power: {artifact.power}"
        + (f", healing: {artifact.healing_power}" if artifact.healing_power > 0 else "")
        + ")"
    )


def main():
    unholy_grenade = Artifact[Unholy, None](
        name="Holy Hand Grenade of Antioch",
        power=1000,
    )

    normal_grenade = bless_artifact(unholy_grenade)

    blessed_grenade = bless_artifact(
        bless_artifact(normal_grenade)
    )  # again, mypy will catch this but now code is much more simple!
