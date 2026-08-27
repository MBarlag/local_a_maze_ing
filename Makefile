
all:
# gonna install conda and make conda env
env: conda_requirements.txt
# install python modules using pip install
install: env requirements.txt
clean:
lint:
lint-strict:

.PHONY: all install clean lint lint-strict
