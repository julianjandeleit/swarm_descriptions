import argparse
import logging
import pathlib
import pandas as pd
import time
import os

def arg_to_loglevel(choice):
    if choice == "critical":
        return logging.CRITICAL
    if choice == "info":
        return logging.INFO
    if choice == "debug":
        return logging.DEBUG
    return logging.INFO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='evaluate finetune results dataset. requires valid docker argos install, including setting xhost +local:docker.')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")
    parser.add_argument("datasets", type=pathlib.Path, help="path to pickled datasets dict")
    parser.add_argument("--workdir", type=pathlib.Path, help="directory to place individual datasets into. Will be crated if not exists.", default="/tmp/datasets")

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
    
    
    
    