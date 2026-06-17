
NAME = a_maze_ing.py
ARGS = config.txt

REQUIREMENTS = requirements.txt

VENV = venv
BIN = $(VENV)/bin
PYTHON = python3

CACHE = $(VENV) .mypy_cache

run: install
	$(BIN)/$(PYTHON) $(NAME) $(ARGS)

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(BIN)/pip install --quiet -r $(REQUIREMENTS)
	$(BIN)/pip install --quiet --upgrade pip

debug: install
	$(BIN)/$(PYTHON) -m pdb $(NAME) $(ARGS)

build: install
	python -m build

clean:
	rm -rf $(CACHE)
	find . -regex '^.*\(__pycache__\|\.py[co]\)$' -delete

lint: install
	source venv/bin/activate\
	&& flake8 .\
	&& mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports\
		--disallow-untyped-defs --check-untyped-defs

lint-strict: install
	source venv/bin/activate\
	&& flake8 .\
	&& mypy --strict .

.PHONY = install run debug build clean lint lint-strict
