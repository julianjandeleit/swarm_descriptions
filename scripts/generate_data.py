import numpy as np
import logging
import yaml
import argparse
import pathlib
import sys
from swarm_descriptions import missions
from swarm_descriptions import descriptions
from swarm_descriptions.configfiles import ET, Configurator, config_to_string
from swarm_descriptions.utils import sample_describer_missions


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

    parser.add_argument('output',
                        help='"description", "config", "write-mission", "read-mission"')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")
    parser.add_argument("--template", type=pathlib.Path, help="path to template argos file",
                        default="ressources/skeleton.argos")

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))

    if args.output == "description":

        dm_modules = [
            (missions.aggregation, descriptions.aggregation),
            (missions.flocking, descriptions.flocking),
        ]

        describer, params = sample_describer_missions(dm_modules)
        description = describer(params)

        print(description)

    elif args.output == "config":
        skeleton = ET.parse(args.template).getroot()
        config = Configurator().generate_config(
            skeleton, missions.aggregation.get_mission(missions.aggregation.sample_params()))
        print(config_to_string(config))

    elif args.output == "write-mission":
        print(yaml.dump(missions.aggregation.get_mission()))

    elif args.output == "read-mission":
        yml = sys.stdin.readlines()
        yml = "".join(yml)
        logging.debug(yml)
        mission = yaml.load(yml, Loader=yaml.Loader)
        logging.info(mission)
