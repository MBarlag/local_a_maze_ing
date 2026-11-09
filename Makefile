VENV_DIR:=.venv
WHICH_UV:=$(shell which uv)
PIP_REQUIREMENTS:=dev_config/requirements.txt
PY_VERSION:=dev_config/.python_v
LINT_FLAGS:=--warn-return-any \
--warn-unused-ignores \
--ignore-missing-imports \
--disallow-untyped-defs \
--check-untyped-defs
PY_VER:=$(shell cat $(PY_VERSION))
CONFIG:=config.txt

all: run
lint:
	$(MAKE) ready
	mypy $(LINT_FLAGS) . || true
	flake8 . || true

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
	uv venv --python $(PY_VER) --link-mode=copy --refresh

# make sure the environment is up to date
# and create a file "ready" when its ready
# to avoid relinking
ready: $(VENV_DIR) $(PIP_REQUIREMENTS) mazegen
	uv pip install --exact -r $(PIP_REQUIREMENTS) --link-mode=copy --refresh
	touch ready

# command asked in subject
# does same as make ready
install:
	$(MAKE) ready

run:
	$(MAKE) ready
	echo $(PY_VER)
	uv run --link-mode=copy --refresh --python $(PY_VER) a_maze_ing.py config.txt

debug:
	$(MAKE) ready
	uv run --link-mode=copy --refresh --python $(PY_VER) -m pdb a_maze_ing.py $(CONFIG)

clean:
	find -not -path "*.venv*" -name __pycache__ | xargs -n1 rm -rf
	find -not -path "*.venv*" -name .mypy_cache | xargs -n1 rm -rf
	find -not -path "*.venv*" -name .ruff_cache | xargs -n1 rm -rf
	find -not -path "*.venv*" -name .pytest_cache | xargs -n1 rm -rf
	find -not -path "*.venv*" -name "*.egg-info" | xargs -n1 rm -rf
	find -path "*tests/output*" -name "*.txt" | xargs -n1 rm -rf
	find -maxdepth 1 -name "*.txt" -and -not -name "config.txt" | xargs -n1 rm -rf
	rm -rf maze
	rm -rf dist
# removes uv package manager, and it's .venv/
# also removes build folders and the file ready

# uninstall:
# 	dev_config/uv_uninstall.sh
# 	$(MAKE) clean
# 	rm -rf $(VENV_DIR)
# 	rm -rf dist
# 	rm -rf *.egg-info
# 	rm -f ready

.PHONY:	all install run debug clean lint lint-strict # uninstall
