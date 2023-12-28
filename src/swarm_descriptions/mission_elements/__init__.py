from dataclasses import dataclass
import random
from swarm_descriptions.configfiles import Configurator
from swarm_descriptions.datamodel import Mission

from swarm_descriptions.mission_elements.datatypes import *
from .arena import CircularArena, RectangularArena
from .lights import UniformLights
from .robots import CenteredSwarm
from .objectives import Foraging, Connection, Aggregation, Distribution
from swarm_descriptions.datamodel import Environment as DMEnv
from swarm_descriptions.datamodel import ObjectiveFunction as DMObj

def get_generators():
    arena_elements = [CircularArena, RectangularArena]
    light_elements = [UniformLights]
    robot_elements = [CenteredSwarm]
    objective_elements = [Foraging, Connection, Aggregation, Distribution]
    
    return arena_elements, light_elements, robot_elements, objective_elements

def sample_element(elements):
        return random.sample(elements, 1)[0]



@dataclass
class MissionParams:
    arena_params: Arena
    lights_params: Lights
    robots_params: Robots
    objective_params: Objective
    
    def sample(arena_elements, light_elements, robot_elements, objective_elements):
        arena_generator = sample_element(arena_elements)
        lights_generator = sample_element(light_elements)
        robots_generator = sample_element(robot_elements)
        objective_generator = sample_element(objective_elements)

        arena = arena_generator.sample()
        generator = MissionParams(
            arena, lights_generator.sample(arena.available_space()), robots_generator.sample(arena.available_space()), objective_generator.sample(arena.available_space()))   
        return generator
    
    def describe(self):
        ads = self.arena_params.describe()
        lds = self.lights_params.describe()
        rds = self.robots_params.describe()
        ods = self.objective_params.describe()
        
        return [ad+ld+rd+od for ad in ads for ld in lds for rd in rds for od in ods]

    def configure(self):
        env = self.arena_params.environment()
        _avs = self.arena_params.available_space()
        walls = self.arena_params.configure()

        lights = self.lights_params.configure()
        robots = self.robots_params.configure()
        obj = self.objective_params.configure()
        obj.spawn_radius = robots.radius

        mission = Mission(
            environment=DMEnv((env.width, env.length, env.height),
                              lights=lights, walls=walls),
            swarm=robots.to_swarm(),
            objective=obj)

        argos_params = Configurator().generate_config_params(mission)
        return argos_params