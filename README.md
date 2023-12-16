# Generating a Dataset of Natural Language Swarm Descriptions and corresponding Robot Controllers

# Installation
For installation, the [Hatch Project Manager](https://hatch.pypa.io/latest/) is recommended.
Hatch can be installed with `pipx install hatch`, assuming [pipx](https://github.com/pypa/pipx) is installed. Pipx can be installed using most package managers or with `python -m pip install --user pipx`. Make sure to execute `pipx ensurepath` after installation.

# Scripts
Run scripts like `hatch run python scripts/generate_data.py -h`.

config files can be run with automode with `/opt/argos/AutoMoDe/bin/automode_main_bt -c /tmp/test.argos --bt-config --nroot 3 --nchildroot 1 --n0 0 --nchild0 2 --n00 6 --c00 5 --p00 0.26 --n01 5 --a01 0 --rwm01 5 --p01 0
` if installed at given path.

# Related Work
 - Towards an integrated automatic design process for robot swarms](https://open-research-europe.ec.europa.eu/articles/1-112/v2) by Bozhinoski et. al.

# Affiliation
This work is part of my masters project at the University of Konstanz.

# Troubleshooting
 
  - `hatch shell` cannot install wheel:  python-version in pyproject.toml needs to be in the shape of _">=3.10"_ and **not** _"==3.10.12"_. At least on Windows.
