VENV_DIR:=.venv
WHICH_UV:=$(shell which uv)
PIP_REQUIREMENTS:=requirements.txt
PY_VERSION:=.python_v
LINT_FLAGS:=--warn-return-any \
--warn-unused-ignores \
--ignore-missing-imports \
--disallow-untyped-defs \
--check-untyped-defs
PY_VER:=$(shell cat $(PY_VERSION))

all: run
lint:
	$(MAKE) ready
	uvx mypy $(LINT_FLAGS) . || true
	uvx flake8 --exclude $(VENV_DIR) . || true

lint-strict:
	$(MAKE) ready
	uvx mypy  --strict . || true
	uvx flake8 --exclude $(VENV_DIR) . || true


# command for installing uv in case it's not installed
# we know it by running which uv
# if its empty, it means uv is not installed
uv_install: $(WHICH_UV)
ifeq ($(WHICH_UV),)
	curl -LsSf https://astral.sh/uv/install.sh | sh
endif

# recepie for creating venv, depends on python version,
# which is stored in a file and any time the file gets updated
# we should delete previous venv if it was there and recreate using
# new python version
$(VENV_DIR): $(PY_VERSION)
	$(MAKE) uv_install
	rm -rf $(VENV_DIR)
	uv venv --python $(PY_VER)

# make sure the environment is up to date
# and create a file "ready" when its ready
# to avoid relinking
ready: $(VENV_DIR) $(PIP_REQUIREMENTS)
	uv pip install --exact -r $(PIP_REQUIREMENTS)
	touch ready

# command asked in subject
# does same as make ready
install:
	$(MAKE) ready

run:
	$(MAKE) ready
	echo $(PY_VER)
	uv run --python $(PY_VER) test.py

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache

# removes uv package manager, and it's .venv
# also removes build folders and the file ready

# uninstall:
# 	./uv_uninstall.sh
# 	$(MAKE) clean
# 	rm -rf $(VENV_DIR)
# 	rm -rf dist
# 	rm -rf *.egg-info
# 	rm -f ready

.PHONY:	all install run clean lint lint-strict # uninstall
