#!/bin/bash -li

echo "Updating Python Env"

shopt -s expand_aliases
source /home/gabe/.bashrc

conda init bash

cd /home/gabe/GoogleDrive/portfolio/python/simulations/
conda activate free_body_sims
conda env export > simulations_environment_ubuntu2204.yml
