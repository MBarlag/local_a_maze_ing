SHELL:= /bin/bash
CONDA_ENV:= amazing
PIP:=
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

$(MINIFORGE_INSTALL):
	curl -L -O $(MINIFORGE_URL)

env: $(CONDA_DIR) $(CONDA_REQUIREMENTS) $(MINIFORGE_INSTALL)

$(CONDA_DIR):
	bash $(MINIFORGE_INSTALL) -b -f -p ${HOME}/conda
	printf ${HOME}/conda/etc/profile.d/conda.sh
	source "${HOME}/conda/etc/profile.d/conda.sh" ; conda activate ; conda activate ; conda create -y -n amazing --file $(CONDA_REQUIREMENTS) ; conda activate amazing

install: env $(PIP_REQUIREMENTS)
	$(PIP) install -r $(PIP_REQUIREMENTS)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache


.PHONY: all env install clean lint lint-strict
