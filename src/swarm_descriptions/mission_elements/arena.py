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
        return [f"{self.radius}"]

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
        return [f"{self.length}, {self.width}"]

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
