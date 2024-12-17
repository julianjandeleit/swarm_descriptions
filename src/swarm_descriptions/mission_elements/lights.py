from dataclasses import dataclass
import logging
from typing import Dict, Optional, List, Tuple
from typing_extensions import Self
import random
from swarm_descriptions.datamodel import Light, Pose
from swarm_descriptions.mission_elements.datatypes import AvailableSpace, Lights, Objective
from swarm_descriptions.mission_elements.objectives import Aggregation, Connection, Distribution, Foraging


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
    def sample(availableSpace: AvailableSpace | None, objective: Objective) -> Self:
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

@dataclass
class TargetLights(Lights):
    lights: List[LightConfig]

    def describe(self) -> List[str]:
        if len(self.lights) == 0:
            return [
    "The area is entirely without lighting.",
    "There are no lights available in the region.",
    "There are 0 lights in the arena.",
    "On the ground, zero lights are present.",
    "The absence of lights results in a dark environment within the arena.",
    "No lighting is present in the arena at this time."
]
        basic_lights = [
    # f"There are {len(self.lights)} lights in the arena located at the following coordinates: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    # f"In this setting, {len(self.lights)} lights are positioned at coordinates: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    # f"The field is illuminated by {len(self.lights)} lights, which can be found at: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    # f"{len(self.lights)} lights are placed throughout the area, with their coordinates being: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    # f"The space is lit with {len(self.lights)} lights, situated at the following positions: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    f"In this terrain, {len(self.lights)} lights are arranged, located at coordinates: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    f"Throughout the environment, there are {len(self.lights)} lights found at these coordinates: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    f"The following lights are present in the arena at coordinates: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    f"The area features {len(self.lights)} lights, positioned at the following coordinates: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])}).",
    f"{len(self.lights)} lights illuminate the space, located at: ({', '.join([f'({light.x}, {light.y})' for light in self.lights])})."
        ]
        
        objective = self.objective
        obj_lights = []
        
        if type(objective) == Aggregation:
            target_area = objective.ground_area_1 if objective.agg_target == 1 else objective.ground_area_2
            obj_lights.append(f"There is a light positioned at the target.")
            obj_lights.append(f"At the {target_area.color.name.lower()} circle is a light.")
            obj_lights.append(f"A light shows the way to the {target_area.color.name.lower()} area.")
            obj_lights.append(f"There is a light shining at the target location.")
            obj_lights.append(f"A light is situated within the {target_area.color.name.lower()} circle.")
        if type(objective) == Distribution:
            
            division = self.division
            lr = objective.area_length/division
            wr = objective.area_width/division
            obj_lights.append(f"There are 4 lights positioned in a rectangle.")
            obj_lights.append(f"At each corner of a rectangle, a light is placed. It has 1/{division} the size of the dimensions the robots should distribute within.")
            obj_lights.append(f"Within a distance of {lr}, 2 lights are placed. 2 more lights are positioned {wr} further away, forming a rectangle with the other lights.")
            obj_lights.append(f"At each corner of the rectangle, a light is placed to ensure even illumination.")
            obj_lights.append(f"Forming a rectangle a {division}th of the target dimensions, 4 lights are placed with a distance of {lr} and {wr} in each dimension.")
            
        if type(objective) == Connection:
            start_area = objective.ground_area_1 if objective.conn_start == objective.ground_area_1.color.name.lower() else objective.ground_area_2
            end_area = objective.ground_area_1 if objective.conn_end == objective.ground_area_1.color.name.lower() else objective.ground_area_2
            obj_lights.append(f"At each circle, a light is positioned")
            obj_lights.append(f"A light is positioned at the target circle. Another light is positioned at the end.")
            obj_lights.append(f"A light is positioned at the coordinates ({self.lights[0].x}, {self.lights[0].y}) with an intensity of {self.lights[0].intensity}.")
            obj_lights.append(f"Another light is located at ({self.lights[1].x}, {self.lights[1].y}), providing an intensity of {self.lights[1].intensity}.")
            obj_lights.append(f"A light is positioned at the {start_area.color.name.lower()} area, while the second is at the {end_area.color.name.lower()} circle. The lights positions are ({self.lights[0].x}, {self.lights[0].y}) and ({self.lights[1].x}, {self.lights[1].y}).")
            
        if type(objective) == Foraging:
            obj_lights.append(f"At each collection area, a light is positioned to assist foragers.")
            obj_lights.append(f"A light is positioned at the collection area, while another light is positioned at a the sink area.")
            obj_lights.append(f"A light is positioned at the coordinates ({self.lights[0].x}, {self.lights[0].y}) to illuminate the first area, and another light is at the second circle at ({self.lights[1].x}, {self.lights[1].y}).")
            obj_lights.append(f"The first light is located at ({self.lights[0].x}, {self.lights[0].y}), guiding foragers, while the second light is at ({self.lights[1].x}, {self.lights[1].y}), providing additional visibility for the other circle.")
            obj_lights.append(f"The lights' positions are ({self.lights[0].x}, {self.lights[0].y}) and ({self.lights[1].x}, {self.lights[1].y}).")
    
        return basic_lights + obj_lights

    @staticmethod
    def sample(availableSpace: AvailableSpace | None, objective: Objective) -> Self:
        lights = []
        division = None
        
        if type(objective) == Aggregation:
            target_area = objective.ground_area_1 if objective.agg_target == 1 else objective.ground_area_2
            lights.append(LightConfig(target_area.pos[0],target_area.pos[1],random.uniform(2.0, 12.0)))
        if type(objective) == Distribution:
            division = random.uniform(1.0, 3.0)
            lr = objective.area_length/division
            wr = objective.area_width/division
            
            lights.append(LightConfig(-lr,-wr,random.uniform(2.0, 12.0)))
            lights.append(LightConfig(lr,-wr,random.uniform(2.0, 12.0)))
            lights.append(LightConfig(-lr,wr,random.uniform(2.0, 12.0)))
            lights.append(LightConfig(lr,wr,random.uniform(2.0, 12.0)))
        if type(objective) == Connection:
            start_area = objective.ground_area_1 if objective.conn_start == objective.ground_area_1.color.name.lower() else objective.ground_area_2
            end_area = objective.ground_area_1 if objective.conn_end == objective.ground_area_1.color.name.lower() else objective.ground_area_2
            lights.append(LightConfig(start_area.pos[0],start_area.pos[1],random.uniform(2.0, 12.0)))
            lights.append(LightConfig(end_area.pos[0], end_area.pos[1],random.uniform(2.0, 12.0)))
            
        if type(objective) == Foraging:
            lights.append(LightConfig(objective.ground_area_1.pos[0],objective.ground_area_1.pos[1],random.uniform(2.0, 12.0)))
            lights.append(LightConfig(objective.ground_area_2.pos[0], objective.ground_area_2.pos[1],random.uniform(2.0, 12.0)))
            
                
        f = TargetLights(lights=lights)
        f.objective = objective
        f.division = division
        return f

    def configure(self) -> Dict[str, Light]:
        lights = [Light(Pose((light.x, light.y, 0.0), (360, 0, 0)),
                        light.intensity) for light in self.lights]
        lights = {f"light_{i}": light for i, light in enumerate(lights)}
        return lights