import random
from typing import List
from typing_extensions import Self
from swarm_descriptions.datamodel import ObjAggregation, ObjectiveFunction, ObjConnection, ObjDistribution, ObjForaging
from swarm_descriptions.mission_elements.datatypes import Objective, Ground, GroundColor
from swarm_descriptions.datamodel import Ground as DMGround

from dataclasses import dataclass

from swarm_descriptions.utils import AvailableSpace


@dataclass
class Aggregation(Objective):
    agg_target: int # if area 1 or 2 is target
    ground_area_1: Ground
    ground_area_2: Ground

    def describe(self) -> List[str]:
        agg_target = self.ground_area_1.color.name.lower() if self.agg_target == 1 else self.ground_area_2.color.name.lower()
        return [
            f"There is a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The objective is for the robots to aggregate at the {agg_target} circle. ",
            f"The goal is for the robots to aggregate at the {agg_target} circle. There are two areas on the floor: a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. ",
            f"The primary goal for the robots is to cluster at the {agg_target} circle. There are two designated areas on the floor: a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. ",
            f"The robots' task is to aggregate at the {agg_target} circle. There are two floor areas, each defined by a circle. The first circle, located at {self.ground_area_1.pos}, has a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}. The second circle, positioned at {self.ground_area_2.pos}, has a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. ",
            f"The robots' goal is to meet at the {agg_target} circle. In the arena, you'll find two areas: a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters. ",
            f"The objective is for the robots to aggregate at the {agg_target} circle. There are two designated areas on the floor: a circle at {self.ground_area_1.pos} in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} in {self.ground_area_2.color.name.lower()}. ",
            f"In the floor space, you'll discover two distinct areas: a circle at {self.ground_area_1.pos} in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} in {self.ground_area_2.color.name.lower()}. The primary objective for the robots is to aggregate at the {agg_target} circle. ",
            f"The primary goal for the robots is to aggregate at the {agg_target} circle. There are two floor areas, each defined by a circle. The first circle has a radius of {self.ground_area_1.radius} meters and the color {self.ground_area_1.color.name.lower()}. The second circle has a radius of {self.ground_area_2.radius} meters and is {self.ground_area_2.color.name.lower()}. ",
            f"In the arena, you'll find two areas: a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The robots' goal is to group together at the {agg_target} circle. ",
            f"The objective is for the robots to aggregate at the {agg_target} circle. There are two designated areas on the floor: a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. "
        ]

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
        return [
            f"There is a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The objective for the robots is to form a line from the {self.conn_start} to the {self.conn_end} circle, so that they connect both circles. While forming a line, the robots should keep a distance of just under {self.conn_range} m. The robots with neighbors below this range count as connected. ",
            f"The objective for the robots is to connect both circles from {self.conn_start} to {self.conn_end}, maintaining a distance just under {self.conn_range} m. There are two circles on the floor—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. ",
            f"The goal for the robots is to create a connection from the {self.conn_start} to the {self.conn_end} circle, maintaining a distance just under {self.conn_range} m. In the floor space, two circles stand out—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. ",
            f"To connect both circles from {self.conn_start} to {self.conn_end} is the objective for the robots, maintaining a distance just under {self.conn_range} m. Imagine two circles on the floor—one centered at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. ",
            f"Picture two circles—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The objective for the robots is to form a connection from the {self.conn_start} to the {self.conn_end} circle while maintaining a distance of just under {self.conn_range} m. ",
            f"There are two circles on the floor—one centered at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The mission for the robots is to connect both circles from {self.conn_start} to {self.conn_end}, keeping a distance just under {self.conn_range} m. ",
            f"Visualize two circles—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, adorned in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters, donned in {self.ground_area_2.color.name.lower()}. The robots' goal is to create a connection from the {self.conn_start} to the {self.conn_end} circle, maintaining a distance just under {self.conn_range} m. ",
            f"In the floor space, two circles stand out—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The robots' objective is to create a connection from the {self.conn_start} to the {self.conn_end} circle while maintaining a distance just under {self.conn_range} m. ",
            f"Imagine two circles on the floor—one centered at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The challenge for the robots is to connect both circles from {self.conn_start} to {self.conn_end}, keeping a distance just under {self.conn_range} m. ",
            f"There are two circles on the floor—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The objective for the robots is to connect both circles from {self.conn_start} to {self.conn_end}, maintaining a distance just under {self.conn_range} m. "
        ]

    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        t1, t2 = random.sample([1, 2], 2)
        g1, g2 = random.sample([1, 2], 2)
        conn_range = random.uniform(0.05, 0.5)
        g1 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.5), color=GroundColor(g1))
        g2 = Ground([random.uniform(availableSpace.min_x, availableSpace.max_x), random.uniform(
            availableSpace.min_y, availableSpace.max_y)], radius=random.uniform(0.25, availableSpace.radius()*0.5), color=GroundColor(g2))

        return Connection(conn_start=GroundColor(t1).name.lower(), conn_end=GroundColor(t2).name.lower(), conn_range=conn_range, ground_area_1=g1, ground_area_2=g2)

    def configure(self) -> ObjectiveFunction:
        grounds = {"ground_1": DMGround(self.ground_area_1.pos, self.ground_area_1.radius, self.ground_area_1.color), "ground_2": DMGround(
            self.ground_area_2.pos, self.ground_area_2.radius, self.ground_area_2.color)}
        return ObjConnection(self.conn_start, self.conn_end, self.conn_range, grounds=grounds)


@dataclass
class Distribution(Objective):
    max_connection_range: float
    area_width: float
    area_length: float

    def describe(self) -> List[str]:
        return [f"The objective of the mission is, that the robots cover an area with length {self.area_length} m and width {self.area_width} m while staying connected. Two robots are connected if their distance is below {self.max_connection_range}. ",
                f"The robots should keep a pairwise distance not larger than {self.max_connection_range} and cover an area of {self.area_width} x {self.area_length} m². ",
                f"The objective for the swarm is to cover an area of {self.area_width} by {self.area_length}, while staying connected to each other. The swarm counts as connected if every robot is transitively connected to each other robot in the swarm. Two robots are connected if their distance is at or below {self.max_connection_range} m. ",
                f"The mission's objective is for the robots to cover an area with a length of {self.area_length} meters and a width of {self.area_width} meters, all while staying connected. Two robots are considered connected if their distance is below {self.max_connection_range} meters. ",
                f"To accomplish the task, the robots must maintain a pairwise distance not exceeding {self.max_connection_range} meters while covering an area of {self.area_width} by {self.area_length} square meters. ",
                f"The swarm's goal is to cover an area of {self.area_width} by {self.area_length} meters while ensuring connectivity. ",
                f"Covering an area of {self.area_width} meters by {self.area_length} meters is the primary objective for the swarm, with the added requirement of maintaining connectivity. Robots are considered connected if their distance is at or below {self.max_connection_range} meters. ",
                f"The mission's aim is for the robots to stay pairwise connected, ensuring their distance is not larger than {self.max_connection_range} meters, while covering an area of {self.area_width} x {self.area_length} square meters. ",
                f"The swarm's mission is to cover an area of {self.area_width} meters by {self.area_length} meters while staying connected. Connectivity is defined such that every robot is transitively connected to each other, and two robots are connected if their distance is at or below {self.max_connection_range} meters. ",
                f"The primary objective for the swarm is to cover an area of {self.area_width} by {self.area_length} meters while maintaining connectivity. "
                ]

    @staticmethod
    def sample(availableSpace: AvailableSpace) -> Self:
        width = random.uniform(
            0.5, availableSpace.max_x - availableSpace.min_x)
        length = random.uniform(
            0.5, availableSpace.max_y - availableSpace.min_y)
        mr = random.uniform(0.05, min(width, length)/2.0)

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
        return [f"There is a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters in {self.ground_area_1.color.name.lower()}, and another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The objective for the robots is to bring items from the {self.start_area} start area to the {self.target_area} circle. ",
                f"Two circles are present—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The robots' task is to transport items from the {self.start_area} starting area to the {self.target_area} circle. ",
                f"In the environment, you'll find a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, characterized by its {self.ground_area_1.color.name.lower()} hue. There's also another circle at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The robots are assigned the goal of moving items from the {self.start_area} starting zone to the {self.target_area} circle. ",
                f"Present in the space are two circles—one situated at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, adorned in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The robots are tasked with transporting items from the {self.start_area} origing to the {self.target_area} circle. ",
                f"There are two circles within the environment—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, colored in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The goal for the robots is to move items from the {self.start_area} start point to the {self.target_area} circle. ",
                f"In the surroundings, there exists a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, exhibiting a {self.ground_area_1.color.name.lower()} color, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The objective for the robots is to transfer items from the {self.start_area} initial location to the {self.target_area} circle. ",
                f"Two circles adorn the area—one positioned at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters, covered in {self.ground_area_2.color.name.lower()}. The task for the robots is to move items from the {self.start_area} starting point to the {self.target_area} circle. ",
                f"Within this space, you'll encounter two circles—one located at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, displaying a {self.ground_area_1.color.name.lower()} shade, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters in {self.ground_area_2.color.name.lower()}. The assigned task for the robots is to transport items from the {self.start_area} origin to the {self.target_area} circle. ",
                f"Observe a circle at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, adorned in {self.ground_area_1.color.name.lower()}, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters, characterized by its {self.ground_area_2.color.name.lower()} hue. The robots' foraging mission is to convey items from the {self.start_area} starting location to the {self.target_area} circle. ",
                f"Two circles are situated in this space—one at {self.ground_area_1.pos} with a radius of {self.ground_area_1.radius} meters, exhibiting a {self.ground_area_1.color.name.lower()} color, and another at {self.ground_area_2.pos} with a radius of {self.ground_area_2.radius} meters, covered in {self.ground_area_2.color.name.lower()}. The robots are assigned the task of transporting items from the {self.start_area} source location to the {self.target_area} sink. "
                ]

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
        grounds = {"ground_1": DMGround(self.ground_area_1.pos, self.ground_area_1.radius, self.ground_area_1.color), "ground_2": DMGround(
            self.ground_area_2.pos, self.ground_area_2.radius, self.ground_area_2.color)}
        return ObjForaging(start=self.start_area, end=self.target_area, grounds=grounds)
