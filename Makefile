CONDA_ENV:= amazing
PIP:= # Path to pip3.
MINIFORGE_INSTALL:= Miniforge3-$(uname)-$(uname -m).sh
MINIFORGE_URL:= "https://github.com/conda-forge/miniforge/releases/latest/download/$(MINIFORGE_INSTALL)"
# OS:= uname
CONDA_REQUIREMENTS:=conda_requirements.txt
PIP_REQUIREMENTS:=requirements.txt


all:
# # gonna install conda and make conda env
# env: conda_requirements.txt
# # install python modules using pip install
# install: env requirements.txt
# clean:
lint:
lint-strict:


env: $(CONDA_REQUIREMENTS)
	curl -L -O $(MINIFORGE_URL)
	bash $(MINIFORGE_INSTALL) -b -f -p ${HOME}/conda

	source ${HOME}/conda/etc/profile.d/conda.sh
	conda activate
	conda create -n amazing --file $(CONDA_REQUIREMENTS)
	activate amazing

install: env $(PIP_REQUIREMENTS)
	$(PIP) install --file $(PIP_REQUIREMENTS)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache


.PHONY: all env install clean lint lint-strict
