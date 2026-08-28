#!/bin/bash

bash $1 -b -f -p $HOME/conda
# printf $HOME/conda/etc/profile.d/conda.sh
source "$HOME/conda/etc/profile.d/conda.sh"
conda activate
conda create -y -n amazing --file $2
conda activate amazing

