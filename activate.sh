#!/bin/bash
ROOT=$(pwd)
source .venv/bin/activate
alias ruff="ruff --config $ROOT/dev_config/ruff.toml"
