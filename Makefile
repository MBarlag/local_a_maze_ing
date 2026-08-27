CONDA_ENV:= amazing
PIP:= # Path to pip3.
MINIFORGE_INSTALL:= Miniforge3-$(uname)-$(uname -m).sh
MINIFORGE_URL:= "https://github.com/conda-forge/miniforge/releases/latest/download/$(MINIFORGE_INSTALL)"
# OS:= uname



all:
# gonna install conda and make conda env
env: conda_requirements.txt
# install python modules using pip install
install: env requirements.txt
clean:
lint:
lint-strict:


env: conda_requirements.txt
	curl -L - O $(MININFORGE_URL)
	bash $(MINIFORGE_INSTALL) 
	conda create -n amazing python=3.10
	activate amazing
	$(PIP) install --file conda_requirements.txt

install: env_requirements.txt

clean:
	rm -rf __pycache__


.PHONY: all env install clean lint lint-strict
