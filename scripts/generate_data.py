import numpy as np
import logging
import yaml
import argparse
import pathlib
import sys
from swarm_descriptions import missions
from swarm_descriptions import descriptions
from swarm_descriptions.configfiles import ET, Configurator, config_to_string
from swarm_descriptions.utils import sample_describer_missions, save_mission_dataset
import pandas as pd
from dataclasses import asdict

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
                        help='"description", "config", "write-mission", "read-mission", "dataset"')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")
    parser.add_argument("--template", type=pathlib.Path, help="path to template argos file",
                        default="ressources/skeleton.argos")
    
    parser.add_argument("--N", type=int, default=None, help="number of rows to generate for dataset")
    parser.add_argument("--out", type=pathlib.Path, default=None, help="output path of generated dataset")

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))

    dm_modules = [
        (missions.aggregation, descriptions.aggregation),
        (missions.flocking, descriptions.flocking),
        (missions.foraging, descriptions.foraging),
        (missions.distribution, descriptions.distribution),
        (missions.connection, descriptions.connection)
    ]

    describer, get_mission, params, labels = sample_describer_missions(dm_modules)
    logging.info(f"sampled {labels}")
    
    if args.output == "description":

        description = describer(params)
        print(description)

    elif args.output == "config":
        skeleton = ET.parse(args.template).getroot()
        config = Configurator().generate_config(
            skeleton, get_mission(params))
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