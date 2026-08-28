#!/bin/bash

# logic of installing the pip3 dependencies
# [run from mac bash conda activate amazing and then which pip3 command ]
source "$HOME/conda/etc/profile.d/conda.sh"
conda activate amazing
pip3 install -r $1