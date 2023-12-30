import argparse
import logging
import pathlib
import pandas as pd
import os
import subprocess
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='evaluate finetune results dataset. requires valid docker argos install, including setting xhost +local:docker.')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")
    parser.add_argument("dataset", type=pathlib.Path)
    parser.add_argument("--template", type=pathlib.Path, default=pathlib.Path("ressources/skeleton.argos"))
    parser.add_argument("--docker", type=pathlib.Path, default=pathlib.Path("/opt/argos/custom/docker"))
    parser.add_argument("--mission-out", type=pathlib.Path, default=pathlib.Path("/tmp/mission.argos"))

    args = parser.parse_args()
    logging.basicConfig(level=arg_to_loglevel(args.logging))

    dataset = args.dataset
    logging.info(f"dataset={dataset}")
    dataset = pd.read_pickle(dataset)
    logging.info(f"dataset-columns={dataset.columns}")
    
    skeleton = ET.parse(args.template)
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
    dataset = dataset.dropna()
    os.chdir(args.docker)
    
    # INVALID argos configs
    
    def run_in_argos(config):
        time.sleep(1)
        with open(args.mission_out, "w") as text_file:
            # logging.debug(f"{config=}")
            text_file.write(config)
        process = subprocess.Popen("ARGOS_FILE=/tmp/mission.argos docker-compose up --build", shell=True, stdout=subprocess.PIPE)
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
    
    # successes = [run_in_argos(ac) for ac in dataset.argos_config]
    # share_invalid_configs = sum(successes) / float(len(successes))
    # print(f"{share_invalid_configs=}")
    
    # BLEU Score
    ref = [sentence_bleu([row.configuration], row.response) for i, row in dataset.iterrows()]
    print(ref[0])
    
    # TODO: Additionally add manual Evaluation