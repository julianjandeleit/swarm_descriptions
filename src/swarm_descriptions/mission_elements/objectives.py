import random
from typing import List, Self
from swarm_descriptions.datamodel import ObjAggregation, ObjectiveFunction
from swarm_descriptions.mission_elements.datatypes import Objective, Ground, GroundColor
from swarm_descriptions.datamodel import Ground as DMGround

from dataclasses import dataclass

from swarm_descriptions.utils import AvailableSpace


@dataclass
class Aggregation(Objective):
    agg_target: int
    ground_area_1: Ground
    ground_area_2: Ground

    def describe(self) -> List[str]:
        return ["test"]

    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        t1, _ = random.sample([1, 2], 2)
        g1, g2 = random.sample([1, 2], 2)
        g1 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.05, availableSpace.radius()), color=GroundColor(g1))
        g2 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.05, availableSpace.radius()), color=GroundColor(g2))

        return Aggregation(t1, g1, g2)

    def configure(self) -> ObjectiveFunction:
        target = self.ground_area_1 if self.agg_target == 1 else self.ground_area_2
        return ObjAggregation(radius=target.radius,
                              target_color=target.color.name.lower(), grounds={"ground_1": DMGround(self.ground_area_1.pos, self.ground_area_1.radius, self.ground_area_1.color), "ground_2": DMGround(self.ground_area_2.pos, self.ground_area_2.radius, self.ground_area_2.color)})
