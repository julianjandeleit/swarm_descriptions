# Swarm Descriptions: Creating and Demonstrating a Dataset for Swarm Mission Generation from Natural Language

# Installation
For installation, the [Hatch Project Manager](https://hatch.pypa.io/latest/) is recommended.
Hatch can be installed with `pipx install hatch`, assuming [pipx](https://github.com/pypa/pipx) is installed. Pipx can be installed using most package managers or with `python -m pip install --user pipx`. Make sure to execute `pipx ensurepath` after installation.

From repository level start hatch virtual python environment with `hatch shell` and install python module with `python -m pip install -e .`.

Copy `custom` directory to `/opt/argos/custom/`. Execute `xhost +local:docker` to enable visualization.

# Execution

## Scrips

Run scripts like `python scripts/test.py -h` inside the hatch virtual environment.

 - `generate_data.py` samples descriptions and configurations for demonstration.
 - `parse_eval_datasets.py` converts the dataset generated by the inference notebook for evaluation.
 - `eval_results.py` contains the data for evaluation of the finetuned model.
 - `run_config_params.py` runs configuration params xml generated from dataset (e.g. `generate_data.py`.)
 - `test.py` prints several properties generated from a randomly sampled mission.

## Notebooks:

Finetuning and inference was done on Kaggle.

 - `figures.ipynb` figures and metrics for report.
 - `mistral-finetuning-swarm.ipynb` finetuning the LLM on our dataset. Includes relevant functions on how to generate dataset from our python module.
 - `mistral-inference-swarm.ipynb` generating configuration params from descriptions by fined LLM for evaluation.

# Related Work
 - [Towards an integrated automatic design process for robot swarms](https://open-research-europe.ec.europa.eu/articles/1-112/v2) by Bozhinoski et. al.
 - [Behavior Trees as a Control Architecture in the Automatic Modular Design of Robot Swarms](https://link.springer.com/chapter/10.1007/978-3-030-00533-7_3) by Kuckling et. al.

# Association
This work is part of my masters project at the University of Konstanz. Find the project report at `project_report.pdf`.

# Troubleshooting
 
  - `hatch shell` cannot install wheel:  python-version in pyproject.toml needs to be in the shape of _">=3.10"_ and **not** _"==3.10.12"_. At least on Windows.
