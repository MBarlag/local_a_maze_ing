#!/bin/bash
PIP_REQUIREMENTS="requirements.txt"


# logic of installing the pip3 dependencies
source "${HOME}/conda/etc/profile.d/conda.sh"
conda activate amazing 
pip3 install -r $PIP_REQUIREMENTS