from dataclasses import dataclass
from typing import Dict, List
from swarm_descriptions import utils
from swarm_descriptions.datamodel import Wall
from swarm_descriptions.mission_elements.datatypes import Arena, AvailableSpace, Environment
import math
import random


@dataclass
class CircularArena(Arena):
    radius: float
    height: float
    num_walls: int

    def describe(self) -> List[str]:
        return [
                    f"The environment consists of a circular arena with radius {self.radius}, made out of {self.num_walls} walls. The environment is {self.height} high. ",
                    f"The environment is a circle made out of {self.num_walls} walls. ",
                    f"The environment is a circular arena with radius {self.radius} m. ",
                    f"The arena has a radius of {self.radius} m. ",
                    f"The circular arena, having a radius of {self.radius} meters, is constructed with {self.num_walls} walls. ",
                    f"The environment features a circle composed of {self.num_walls} walls. ",
                    f"In this setting, a circular arena with a radius of {self.radius} meters is established. ",
                    f"The circular arena, constructed with {self.num_walls} walls, has a radius of {self.radius} m. ",
                    f"A circle with {self.num_walls} walls forms the structure of the environment. ",
                    f"With a radius of {self.radius} meters, the circular arena is made up of {self.num_walls} walls. "
                ]

    @staticmethod
    def sample() -> "CircularArena":
        return CircularArena(radius=random.uniform(1.0, 5.0), height=random.uniform(1, 3), num_walls=random.randint(3, 25))

    def environment(self) -> Environment:
        side_length_outer_square = 2*self.radius + 2.0  # with padding 2
        return Environment(side_length_outer_square, side_length_outer_square, self.height)

    def configure(self) -> Dict[str, Wall]:
        walls = {f"wall_{i}": w for i, w in enumerate(
            utils.generate_circular_walls(self.radius, self.num_walls))}
        return walls

    def available_space(self) -> AvailableSpace:
        radius = self.radius
        height = self.height
        # Calculate the largest rectangle that fits inside the circle
        # NOTE: we might have discretizatin error because of limited number of walls
        side_length = math.sqrt(2) * radius
        min_x = -side_length / 2.0
        max_x = side_length / 2.0
        min_y = -side_length / 2.0
        max_y = side_length / 2.0

        min_z = 0
        max_z = height / 2.0
        return AvailableSpace(min_y, max_y, min_x, max_x, min_z, max_z)


@dataclass
class RectangularArena(Arena):
    length: float
    width: float
    height: float

    def describe(self) -> List[str]:
        return [
                    f"The environment consists of a rectangular area with length {self.length}, width {self.width}, and height {self.height}.",
                    f"The area is a rectangle with dimensions {self.length} x {self.width} x {self.height}.",
                    f"The environment is a rectangular area with length {self.length} m, width {self.width} m, and height {self.height} m.",
                    f"The rectangular area has dimensions {self.length} m x {self.width} m x {self.height} m.",
                    f"The environment is constructed as a rectangular space with a length of {self.length} meters, width of {self.width} meters, and height of {self.height} meters.",
                    f"In this setting, a rectangle is formed with dimensions {self.length} x {self.width} x {self.height}.",
                    f"A rectangular area, with a length of {self.length} meters, width of {self.width} meters, and height of {self.height} meters, is established.",
                    f"The rectangular space is {self.length} m long, {self.width} m wide, and {self.height} m high.",
                    f"The environment features a rectangle with dimensions {self.length} x {self.width} x {self.height}.",
                    f"With a length of {self.length} meters, width of {self.width} meters, and height of {self.height} meters, the area is rectangular in shape."
               ]


    @staticmethod
    def sample() -> "RectangularArena":
        length = random.uniform(1.0, 7.5)
        width = random.uniform(1.0, 7.5)
        height = random.uniform(1.0, 3.0)
        return RectangularArena(length, width, height)

    def environment(self) -> Environment:
        return Environment(self.width, self.length, self.height)

    def configure(self) -> Dict[str, Wall]:
        walls = {f"wall_{i}": w for i, w in enumerate(
            utils.generate_square_of_walls(self.width, self.length))}
        return walls

    def available_space(self) -> AvailableSpace:
        length = self.length
        width = self.width
        height = self.height
        min_x = -length / 2.0
        max_x = length / 2.0
        min_y = -width / 2.0
        max_y = width / 2.0

        min_z = 0
        max_z = height / 2.0

        return AvailableSpace(min_y, max_y, min_x, max_x, min_z, max_z) # x, y swapped
