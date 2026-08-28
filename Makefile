SHELL:= /bin/bash
CONDA_ENV:= amazing
PIP:=pip3
OS:=$(shell uname)
ARCH:=$(shell uname -m)
MINIFORGE_INSTALL:= Miniforge3-$(OS)-$(ARCH).sh
MINIFORGE_URL:= "https://github.com/conda-forge/miniforge/releases/latest/download/$(MINIFORGE_INSTALL)"
# OS:= uname
CONDA_REQUIREMENTS:=conda_requirements.txt
PIP_REQUIREMENTS:=requirements.txt
CONDA_DIR:=${HOME}/conda
# HOME_DIR:=$(shell echo "${HOME}")
all:
# # gonna install conda and make conda env
# env: conda_requirements.txt
# # install python modules using pip install
# install: env requirements.txt
# clean:
lint:
lint-strict:

# [thinking to move all of the long commands into one script file, 
# and then just run the script file from makefile]

$(MINIFORGE_INSTALL):
	curl -L -O $(MINIFORGE_URL)

env: $(CONDA_DIR)

$(CONDA_DIR): $(CONDA_REQUIREMENTS)
	$(MAKE) $(MINIFORGE_INSTALL)
	./conda_install.sh $(MINIFORGE_INSTALL) $(CONDA_REQUIREMENTS) 

install: env $(PIP_REQUIREMENTS)
	./install.sh $(PIP_REQUIREMENTS)

run:
	source $(CONDA_DIR)/etc/profile.d/conda.sh ; conda activate amazing ; python3 test.py

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	[delete conda]


.PHONY: all env install clean lint lint-strict
