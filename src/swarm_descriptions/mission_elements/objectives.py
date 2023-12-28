import random
from typing import List, Self
from swarm_descriptions.datamodel import ObjAggregation, ObjectiveFunction, ObjConnection, ObjDistribution, ObjForaging
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
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.5), color=GroundColor(g1))
        g2 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.5), color=GroundColor(g2))

        return Aggregation(t1, g1, g2)

    def configure(self) -> ObjectiveFunction:
        target = self.ground_area_1 if self.agg_target == 1 else self.ground_area_2
        return ObjAggregation(radius=target.radius,
                              target_color=target.color.name.lower(), grounds={"ground_1": DMGround(self.ground_area_1.pos, self.ground_area_1.radius, self.ground_area_1.color), "ground_2": DMGround(self.ground_area_2.pos, self.ground_area_2.radius, self.ground_area_2.color)})


@dataclass
class Connection(Objective):
    conn_start: str
    conn_end: str
    conn_range: float
    ground_area_1: Ground
    ground_area_2: Ground
    
    def describe(self) -> List[str]:
        return ["descrip"]
    
    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        t1, t2 = random.sample([1, 2], 2)
        g1, g2 = random.sample([1, 2], 2)
        conn_range = random.uniform(0.05,0.5)
        g1 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.5), color=GroundColor(g1))
        g2 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.5), color=GroundColor(g2))

        return Connection(conn_start=GroundColor(t1).name.lower(), conn_end=GroundColor(t2).name.lower(), conn_range=conn_range, ground_area_1=g1, ground_area_2=g2)
    
    def configure(self) -> ObjectiveFunction:
        grounds = {"ground_1": DMGround(self.ground_area_1.pos, self.ground_area_1.radius, self.ground_area_1.color), "ground_2": DMGround(self.ground_area_2.pos, self.ground_area_2.radius, self.ground_area_2.color)}
        return ObjConnection(self.conn_start, self.conn_end, self.conn_range, grounds = grounds)
    
    
@dataclass
class Distribution(Objective):
    max_connection_range: float
    area_width: float
    area_length: float
    
    def describe(self) -> List[str]:
        return ["asdf"]
    
    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        width = random.uniform(0.5, availableSpace.max_x - availableSpace.min_x)
        length = random.uniform(0.5, availableSpace.max_y - availableSpace.min_y)
        mr = random.uniform(0.05, min(width,length)/2.0)
        
        return Distribution(mr, width, length)
    
    def configure(self) -> ObjectiveFunction:
        return ObjDistribution([self.area_width, self.area_length], max_connection_distance=self.max_connection_range)
        
@dataclass        
class Foraging(Objective):
    start_area: str
    target_area: str
    ground_area_1: Ground
    ground_area_2: Ground
    
    def describe(self) -> List[str]:
        return ["test"]
    
    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        t1, t2 = random.sample([1, 2], 2)
        g1, g2 = random.sample([1, 2], 2)
        g1 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.25), color=GroundColor(g1))
        g2 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.25), color=GroundColor(g2))

        return Foraging(start_area=GroundColor(t1).name.lower(), target_area=GroundColor(t2).name.lower(), ground_area_1=g1, ground_area_2=g2)
    
    def configure(self) -> ObjectiveFunction:
        grounds = {"ground_1": DMGround(self.ground_area_1.pos, self.ground_area_1.radius, self.ground_area_1.color), "ground_2": DMGround(self.ground_area_2.pos, self.ground_area_2.radius, self.ground_area_2.color)}
        return ObjForaging(start=self.start_area, end=self.target_area, grounds=grounds)