import time
import subprocess
from types import SimpleNamespace
from swarm_descriptions.configfiles import config_to_string, Configurator, ET
from swarm_descriptions.utils import arg_to_loglevel
import logging
import argparse
import pathlib
import os

def config_params_to_argos_config(config_params_path: str, template_path: str, out_path: str):
    with open(config_params_path, 'r') as file:
        params = file.read().replace('\n', '')
    skeleton = ET.parse(template_path)
    xml = ET.fromstring(params)
    config_tree = Configurator().convert_config_params(params=xml, skeleton_root=skeleton)
    config = config_tree.getroot()
    config = config_to_string(config)
    
    with open(out_path, "w") as text_file:
        # logging.debug(f"{config=}")
        text_file.write(config)
    
def run_in_argos(argos_file_path: str, argos_docker_path: str):
    """execute argos
    
    Requires xhost +local:docker to be set.

    Args:
        argos_file_path (str): .argos file file on the file system to be loaded.

    Returns:
        bool: success
    """
    
    time.sleep(1)
    old_dir = os.getcwd()
    os.chdir(argos_docker_path)
    process = subprocess.Popen(f"ARGOS_FILE={argos_file_path} docker-compose up --build", shell=True, stdout=subprocess.PIPE)
    out_lines = []
    for line in iter(process.stdout.readline, ''):
        if line == b'':
            break
        out_lines.append(line.decode("ascii"))
    process.stdout.close()
    process.wait()
    out = "".join(out_lines)
    success = 'code 0' in out
    os.chdir(old_dir)
    time.sleep(1) # allow cleanup time
    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='run config parameters in argos including setting xhost +local:docker.')
    parser.add_argument(
        "--logging", choices=["critical", "info", "debug"], default="info")
    parser.add_argument("config_params", type=pathlib.Path, help="config params that should be run")
    parser.add_argument("--template", type=pathlib.Path,  help="template path",default=pathlib.Path("ressources/skeleton.argos"))
    parser.add_argument("--docker", type=pathlib.Path, help="docker compose directory", default=pathlib.Path("/opt/argos/custom/docker"))
    parser.add_argument("--argos-out", type=pathlib.Path, help="where the converted argos should be written to", default=pathlib.Path("/tmp/mission.argos"))

    args = parser.parse_args()
else:
    args = SimpleNamespace({"logging": "info"})
    
logging.basicConfig(level=arg_to_loglevel(args.logging))

config_params_to_argos_config(args.config_params, args.template, args.argos_out)
success = run_in_argos(args.argos_out, args.docker)
logging.info(f"{success=}")