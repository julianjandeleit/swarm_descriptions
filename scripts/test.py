import argparse
from swarm_descriptions.configfiles import Configurator, config_to_string, ET
from swarm_descriptions.datamodel import Mission
from swarm_descriptions.datamodel import Environment as DMEnv
from swarm_descriptions.datamodel import ObjectiveFunction as DMObj
from swarm_descriptions.mission_elements.arena import *
from swarm_descriptions.mission_elements.lights import *
from swarm_descriptions.mission_elements.robots import *
from swarm_descriptions.mission_elements.objectives import *

def arg_to_loglevel(choice):
    if choice == "critical":
        return logging.CRITICAL
    if choice == "info":
        return logging.INFO
    if choice == "debug":
        return logging.DEBUG
    return logging.INFO

@dataclass
class MissionParams:
    arena_params: Arena
    lights_params: Lights
    robots_params: Robots
    objective_params: Objective

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


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Print generated data')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))

    arena_elements = [CircularArena, RectangularArena]
    light_elements = [UniformLights]
    robot_elements = [CenteredSwarm]
    objective_elements = [Foraging, Connection, Aggregation, Distribution]

    def sample_element(elements):
        return random.sample(elements, 1)[0]

    arena_generator = sample_element(arena_elements)
    lights_generator = sample_element(light_elements)
    robots_generator = sample_element(robot_elements)
    objective_generator = sample_element(objective_elements)

    arena = arena_generator.sample()
    generator = MissionParams(
        arena, lights_generator.sample(arena.available_space()), robots_generator.sample(arena.available_space()), objective_generator.sample(arena.available_space()))

    config_str = config_to_string(generator.configure())
    skeleton = ET.parse("ressources/skeleton.argos").getroot()
    argos_str = Configurator().convert_config_params(generator.configure(), skeleton)
    argos_str = config_to_string(argos_str)
    print(argos_str)
