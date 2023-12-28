from dataclasses import dataclass
import logging
from typing import Dict, Optional, List, Tuple
from typing_extensions import Self
import random
from swarm_descriptions.datamodel import Light, Pose
from swarm_descriptions.mission_elements.datatypes import AvailableSpace, Lights


@dataclass
class LightConfig:
    x: float
    y: float
    intensity: float


@dataclass
class UniformLights(Lights):
    lights: List[LightConfig]

    def describe(self) -> List[str]:
        if len(self.lights) == 0:
            return [f"There are {len(self.lights)} lights distributed evenly in the arena. ", f"{len(self.lights)} lights are distributed uniformly in the arena. "]
        return [
            f"There are {len(self.lights)} lights distributed evenly in the arena. ",
            f"In the arena, {len(self.lights)} lights are evenly spread out with intensities {', '.join([str(light.intensity) for light in self.lights])}. ",
            f"The arena is illuminated by {len(self.lights)} lights evenly distributed across the space. ",
            f"{len(self.lights)} lights are evenly positioned throughout the arena, providing illumination. Their intensities are {', '.join([str(light.intensity) for light in self.lights])}. ",
            f"The space is lit with {len(self.lights)} lights evenly distributed. Positions are ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}). ",
            f"In this setting, {len(self.lights)} lights are placed euniformly in the arena. Light intensities range from {min([light.intensity for light in self.lights])} to {max([light.intensity for light in self.lights])}. ",
            f"Evenly distributed throughout the environment are {len(self.lights)} lights. Their positions are ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}). ",
            f"There are the following lights in the arena: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}). ",
            f"The arena features {len(self.lights)} lights: {', '.join([f'({light.x}, {light.y}, {light.intensity})' for light in self.lights])}. ",
            f"{len(self.lights)} lights are distributed uniformly in the arena. "
        ]

    @staticmethod
    def sample(availableSpace: AvailableSpace | None) -> Self:
        logging.debug(availableSpace)
        num = random.randint(0, 4)
        lights: List[LightConfig] = [LightConfig(
            random.uniform(availableSpace.min_x, availableSpace.max_x),
            random.uniform(availableSpace.min_y, availableSpace.max_y),
            random.uniform(2.0, 8.0)
        ) for n in range(num)]
        f = UniformLights(lights=lights)
        return f

    def configure(self) -> Dict[str, Light]:
        lights = [Light(Pose((light.x, light.y, 0.0), (360, 0, 0)),
                        light.intensity) for light in self.lights]
        lights = {f"light_{i}": light for i, light in enumerate(lights)}
        return lights
