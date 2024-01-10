import argparse
import logging
import pathlib
import pandas as pd
import os
import subprocess
import numpy as np
from swarm_descriptions.configfiles import Configurator, ET, config_to_string
import time
from nltk.translate.bleu_score import sentence_bleu
def arg_to_loglevel(choice):
    if choice == "critical":
        return logging.CRITICAL
    if choice == "info":
        return logging.INFO
    if choice == "debug":
        return logging.DEBUG
    return logging.INFO


def evaluate_dataset(dataset_path, template_path, docker_compose_dir, mission_out_path):
    """Evaluate dataset of single checkpoint

    Args:
        dataset_path (pathlib.Path): dataset as pickeled pd
        template_path (pathlib.Path): path to skeleton.argos
        docker_compose_dir (pathlib.Path): path to docker compose directory that executes argos
        mission_out_path (dict): bleu score, share of invalid config-params, share of invalid argos files (share total of argos files are based on total number of _valid_ config-params)

    Returns:
        dict: Metrics
    """
    dataset = dataset_path
    print(f"{dataset=}")
    dataset = pd.read_pickle(dataset)
    logging.info(f"dataset-columns={dataset.columns}")
    
    skeleton = ET.parse(template_path)
    def response_to_argos_config(params):
        try:
            xml = ET.fromstring(params)
            config_tree = Configurator().convert_config_params(params=xml, skeleton_root=skeleton)
            config = config_tree.getroot()
            config = config_to_string(config)
            return config
        except Exception as _e:
            return None
    
    dataset["argos_config"] = dataset.response.map(response_to_argos_config)
    
    # INVALID config-params
    
    share_nones = dataset.argos_config.apply(lambda x: x == None).sum() / dataset.shape[0]
    print(f"{share_nones=}")
    #dataset = dataset.dropna()
    old_dir = os.getcwd()
    os.chdir(docker_compose_dir)
    
    # INVALID argos configs
    
    def run_in_argos(config):
        time.sleep(1)
        with open(mission_out_path, "w") as text_file:
            # logging.debug(f"{config=}")
            text_file.write(config)
        process = subprocess.Popen("ARGOS_FILE=/tmp/mission.argos docker-compose up --build", shell=True, stdout=subprocess.PIPE) #TODO: ARGOS_FILE needs to be equal to mission out and not hardcoded to specific value
        out_lines = []
        for line in iter(process.stdout.readline, ''):
            if line == b'':
                break
            out_lines.append(line.decode("ascii"))
        process.stdout.close()
        process.wait()
        out = "".join(out_lines)
        success = 'code 0' in out
        time.sleep(1) # allow cleanup time
        return success
    
    dataset["argos_success"] = [run_in_argos(ac) if ac else False for ac in dataset.argos_config]
    if len(dataset) == 0:
        share_invalid_configs = 1.0
    else:
        share_invalid_configs = sum(dataset.argos_success) / float(len(dataset))
    print(f"{share_invalid_configs=}")
    
    # go back to actual working dir to avoid side effects and allow calling multiple times in a row
    os.chdir(old_dir)
    
    # BLEU Score
    if len(dataset) == 0:
        bleu_score_mean = 0.0
        bleu_score_var = 0.0
    else:
        ref = [sentence_bleu([row.configuration], row.response) for i, row in dataset.iterrows()]
        bleu_score_mean = np.mean(ref)
        bleu_score_var = np.var(ref)
    print(f"{bleu_score_mean=}")
    print(f"{bleu_score_var=}")
    
    return {"bleu_score_mean": bleu_score_mean, "bleu_score_var": bleu_score_var,"invalid_config_params": share_nones, "invalid_argos_configs": share_invalid_configs}, dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='evaluate finetune results dataset. requires valid docker argos install, including setting xhost +local:docker.')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")
    parser.add_argument("dataset", type=pathlib.Path, help="Pickled Dataset as pd.DataFrame or directory of those.")
    parser.add_argument("--template", type=pathlib.Path, default=pathlib.Path("ressources/skeleton.argos"))
    parser.add_argument("--docker", type=pathlib.Path, default=pathlib.Path("/opt/argos/custom/docker"))
    parser.add_argument("--mission-out", type=pathlib.Path, default=pathlib.Path("/tmp/mission.argos"))
    parser.add_argument("--result-out", type=pathlib.Path, default=None, help="csv file where result dataframe should be written to")

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))
    
    dataset_path = args.dataset
    template_path = args.template
    docker_compose_dir = args.docker
    mission_out_path = args.mission_out
    result_out_path = args.result_out
    
    ds = []
    if dataset_path.is_dir():
        individual_datasets = list(dataset_path.iterdir())
        logging.info(f"{individual_datasets=}")
        for dataset in individual_datasets:
            res, df = evaluate_dataset(dataset, template_path, docker_compose_dir, mission_out_path)
            res["dataset"] = str(dataset.stem)
            df.to_pickle(dataset)
            ds.append(res)
    else:
        res, df = evaluate_dataset(dataset_path, template_path, docker_compose_dir, mission_out_path)
        res["dataset"] = str(dataset_path.stem)
        df.to_pickle(dataset_path)
        ds.append(res)
        
    if result_out_path:
        logging.info(f"Writing metrics to \"{result_out_path}\"")
        pd.DataFrame(ds).to_csv(result_out_path, index=False)
        
        
    # TODO: Additionally add manual Evaluation