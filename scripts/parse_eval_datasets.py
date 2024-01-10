import argparse
import logging
import pathlib
import pandas as pd
import time
import os
from swarm_descriptions.utils import arg_to_loglevel

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Unpack pickled datasets dictionary. You can leave default arguments for data in ressources directory when called from project level.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], help="log level", default="info")
    parser.add_argument("--datasets", type=pathlib.Path, help="path to pickled datasets dict", default="ressources/data/eval_datasets.pickle")
    parser.add_argument("--workdir", type=pathlib.Path, help="directory to place individual datasets into. Will be crated if not exists.", default="ressources/data/eval_checkpoints/")

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))

    datasets = args.datasets
    logging.info(f"dataset={datasets}")
    datasets = pd.read_pickle(datasets)
    logging.info(f"dataset-columns={datasets.keys()}")
    
    pathlib.Path(args.workdir).mkdir(parents=True, exist_ok=True)
    os.chdir(args.workdir)
    
    checkpoints = list(datasets.keys())
    for cp in checkpoints:
        dataset: pd.DataFrame = datasets[cp]
        dataset.to_pickle(f"{cp}.pickle")
        
    logging.info(f"Checkpoints successfully written to directory \"{args.workdir}\"")
    
    
    
    