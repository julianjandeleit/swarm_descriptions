

from dataclasses import dataclass
from typing import List, Self
from swarm_descriptions.datamodel import RobotSwarm
from swarm_descriptions.mission_elements.datatypes import Robots
from swarm_descriptions.utils import AvailableSpace
import random


@dataclass
class CenteredSwarm(Robots):
    radius: float
    num_robots: int

    def describe(self) -> List[str]:
        return ["descr"]

    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        radius = availableSpace.radius()
        radius = random.uniform(min(0.1, radius), radius)
        num = random.randint(5, 25)
        return CenteredSwarm(radius, num)

    def configure(self) -> RobotSwarm:
        return RobotSwarm(center=(0.0, 0.0), num_robots=self.num_robots,
                          radius=self.radius)
