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

env: $(MINIFORGE_INSTALL) $(CONDA_DIR) $(CONDA_REQUIREMENTS) 

$(CONDA_DIR):
	bash $(MINIFORGE_INSTALL) -b -f -p ${HOME}/conda
	printf ${HOME}/conda/etc/profile.d/conda.sh
	source "${HOME}/conda/etc/profile.d/conda.sh" ; conda activate ; conda activate ; conda create -y -n amazing --file $(CONDA_REQUIREMENTS) ; conda activate amazing

install: env $(PIP_REQUIREMENTS)
	source "${HOME}/conda/etc/profile.d/conda.sh"; conda activate amazing; pip3 install -r $(PIP_REQUIREMENTS)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache


.PHONY: all env install clean lint lint-strict
