from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Generic, TypeVar, List, Dict, Optional
from typing_extensions import Self
from swarm_descriptions.datamodel import GroundColor, Light, ObjectiveFunction, RobotSwarm, Wall

# helper classes

T = TypeVar("T")  # type that configure returns


@dataclass
class MissionElement(ABC, Generic[T]):

    @abstractmethod
    def configure(self) -> T: pass

    @abstractmethod
    def describe(self) -> List[str]: pass

    @staticmethod
    @abstractmethod
    def sample(availableSpace: Optional["AvailableSpace"]) -> Self: pass

    @staticmethod
    @abstractmethod
    def sample() -> Self: pass


@dataclass
class AvailableSpace:
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    min_z: float
    max_z: float

    def radius(self):
        avs = self
        return min(avs.max_x-avs.min_x, avs.max_y-avs.min_y)/2.0


@dataclass
class Environment:
    width: float
    length: float
    height: float


@dataclass
class Ground:
    pos: Tuple[float, float]
    radius: float
    color: GroundColor

# actual abstract classes to override


@dataclass
class Arena(MissionElement[Dict[str, Wall]]):

    @abstractmethod
    def available_space(self) -> AvailableSpace: pass

    @abstractmethod
    def environment(self) -> Environment: pass


@dataclass
class Lights(MissionElement[Dict[str, Light]]):
    pass


@dataclass
class Robots(MissionElement[RobotSwarm]):
    pass


@dataclass
class Objective(MissionElement[ObjectiveFunction]):
    pass
