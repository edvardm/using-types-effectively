from dataclasses import dataclass
from typing import TypeVarTuple, TypeVar, Unpack


@dataclass(frozen=True)
class UnholyArtifact:
    name: str
    power: int


@dataclass(frozen=True)
class UntaintedArtifact:
    name: str
    power: int


@dataclass(frozen=True)
class BlessedArtifact:
    name: str
    power: int


@dataclass(frozen=True)
class RadiantArtifact:
    name: str
    healing_power: int


# Define the state transitions
States = TypeVarTuple("States")
T = TypeVar("T", Unpack[States])


def bless_artifact(artifact: T) -> T:
    """Bless an artifact, transforming it to the next state in the sequence.

    Type system ensures:
    - UnholyArtifact -> UntaintedArtifact
    - UntaintedArtifact -> BlessedArtifact
    """
    match artifact:
        case UnholyArtifact(name=name, power=power):
            return UntaintedArtifact(name=name, power=power)
        case UntaintedArtifact(name=name, power=power):
            return BlessedArtifact(name=name, power=power)


def make_radiant(
    artifact: UntaintedArtifact | BlessedArtifact,
) -> RadiantArtifact:
    match artifact:
        case UntaintedArtifact(name=name, power=power):
            return RadiantArtifact(name=name, healing_power=power)
        case BlessedArtifact(name=name, power=power):
            return RadiantArtifact(name=name, healing_power=power * 2)
