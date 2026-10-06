#!/bin/bash
ROOT=$(pwd)
cd submodules
SRC=$(pwd)
cd $ROOT
export PYTHONPATH=$SRC
source .venv/bin/activate