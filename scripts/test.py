import argparse
from swarm_descriptions.configfiles import Configurator, config_to_string, ET
from swarm_descriptions.datamodel import Mission
from swarm_descriptions.datamodel import Environment as DMEnv
from swarm_descriptions.datamodel import ObjectiveFunction as DMObj
from swarm_descriptions.mission_elements import MissionParams, get_generators
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Print generated data')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))

    arena_elements, light_elements, robot_elements, objective_elements = get_generators()

    generator = MissionParams.sample(*get_generators())

    config_str = config_to_string(generator.configure())
    config_str = utils.truncate_floats(config_str)
    skeleton = ET.parse("ressources/skeleton.argos").getroot()
    argos_str = generator.configure()
    #argos_str = Configurator().convert_config_params(generator.configure(), skeleton)
    #argos_str = generator.configure()
    argos_str = config_to_string(argos_str)
    argos_str = utils.truncate_floats(argos_str)
    print(argos_str)
    print(utils.truncate_floats(random.sample(generator.describe(), 1)[0]))
    print(len(generator.describe()))
