import numpy as np
import logging
import yaml
import argparse
import pathlib
import sys
from swarm_descriptions.configfiles import ET, Configurator, config_to_string
from swarm_descriptions.mission_elements import MissionParams, get_generators
from swarm_descriptions.utils import sample_describer_missions, save_mission_dataset
import pandas as pd
from dataclasses import asdict
import random

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
                        help='"describe", "configure"')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")
    parser.add_argument("--template", type=pathlib.Path, help="path to template argos file",
                        default="ressources/skeleton.argos")
    
    parser.add_argument("--N", type=int, default=None, help="number of rows to generate for dataset")
    parser.add_argument("--out", type=pathlib.Path, default=None, help="output path of generated dataset")
    parser.add_argument("--seed", type=int, default=None, help="seed for random generator. No seed if empty.")

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))
    
    if args.seed is not None:
        logging.info(f"setting seed {args.seed}")
        np.random.seed(args.seed)
        random.seed(args.seed)

    mission = MissionParams.sample(*get_generators())
    logging.info(f"{mission=}")
    
    if args.output == "describe":

        description = random.sample(mission.describe(),1)[0]
        print(description)
        
    elif args.output == "configure":
        skeleton = ET.parse(args.template).getroot()
        # config = Configurator().generate_config(
        #     skeleton, get_mission(params))
        config = mission.configure()
        print(config_to_string(config))
        
    elif args.output == "write-mission":
        print(yaml.dump(missions.aggregation.get_mission()))

    elif args.output == "read-mission":
        yml = sys.stdin.readlines()
        yml = "".join(yml)
        logging.debug(yml)
        mission = yaml.load(yml, Loader=yaml.Loader)
        logging.info(mission)
        
    elif args.output == "dataset":
        n_rows = args.N
        out = args.out
        logging.debug("n_rows="+str(n_rows))
        if not isinstance(n_rows, int):
            logging.error("Number of rows is not valid or not defined. Provide number of rows with -N.")
            exit(1)
            
        if out is None:
            logging.error("Invalid outpath. Provide valid outpath with --out. ")
            exit(1)
        
        rows = []    
        for n in range(n_rows):
            describer, get_mission, params, modules = sample_describer_missions(dm_modules)
            mission_label = modules[0]
            description_label = modules[1]
            
            rows.append({"describer": describer, "get_mission": get_mission, "params_type": params, "params": params, "mission_type": mission_label, "description_type": description_label})

        dataset = pd.DataFrame(rows)
        logging.debug(dataset.params_type.head())
        save_mission_dataset(out, dataset)