from dataclasses import dataclass
from typing import Dict, Optional, Self, List, Tuple
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
        return [f"There are {len(self.lights)} lights distributed evenly in the arena. "]

    @staticmethod
    def sample(availableSpace: AvailableSpace | None) -> Self:

        num = random.randint(0, 6)
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
