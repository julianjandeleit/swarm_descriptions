

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
        return [
                    f"There are {self.num_robots} robots placed uniformly around the center within a radius of {self.radius} meters. ",
                    f"{self.num_robots} robots are evenly distributed around the origin within a radius of {self.radius} m. ",
                    f"Within a {self.radius}-meter radius around the center, {self.num_robots} robots are evenly positioned. ",
                    f"Uniformly distributed are {self.num_robots} robots within a radius of {self.radius} meters. ",
                    f"{self.num_robots} robots are evenly spaced around the central point, spanning a radius of {self.radius} m. ",
                    f"Placed within a {self.radius}-meter radius around the center are {self.num_robots} robots. ",
                    f"Around the central point, {self.num_robots} robots are positioned uniformly within a {self.radius}-meter radius. ",
                    f"{self.num_robots} robots are evenly placed around the center, covering a radius of {self.radius} meters. ",
                    f"Within a {self.radius}-meter radius from the center, {self.num_robots} robots are uniformly distributed. ",
                    f"Evenly positioned around the origin are {self.num_robots} robots within a radius of {self.radius} meters. "
                ]


    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        radius = availableSpace.radius()
        radius = random.uniform(max(0.25, radius/2.0), radius)
        num = random.randint(5, 25)
        return CenteredSwarm(radius, num)

    def configure(self) -> RobotSwarm:
        return RobotSwarm(center=(0.0, 0.0), num_robots=self.num_robots,
                          radius=self.radius)
