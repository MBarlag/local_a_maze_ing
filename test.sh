#!/bin/bash
uv venv --python 3.10 --clear
uv pip install --exact -r req.txt
uv pip list
uv run --python 3.10 test.py
