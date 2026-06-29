
NAME = a_maze_ing.py
ARGS = config.txt

REQUIREMENTS = requirements.txt

PROJECT = a_maze_ing_project
MAZE_PACKAGE = maze_gen
VENV = venv
BIN = $(VENV)/bin
PYTHON = python3

CACHE = .mypy_cache $(PROJECT)/$(MAZE_PACKAGE)/dist output_file

run: install
	$(BIN)/$(PYTHON) $(NAME) $(ARGS)

venv:
	$(PYTHON) -m venv $(VENV)

install: venv
	$(BIN)/pip install --quiet --upgrade pip
	$(BIN)/pip install --quiet -r $(REQUIREMENTS)

debug: install
	$(BIN)/$(PYTHON) -m pdb $(NAME) $(ARGS)

build: install
	$(BIN)/$(PYTHON) -m build $(PROJECT)/$(MAZE_PACKAGE)

clean:
	rm -rf $(CACHE)
	find ./$(PROJECT) | grep -E "(__pycache__|\.pyc$$)" | xargs rm -rf

fclean: clean
	rm -rf $(VENV)

lint: install
	source venv/bin/activate\
	&& flake8 .\
	&& mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports\
		--disallow-untyped-defs --check-untyped-defs

lint-strict: install
	source venv/bin/activate\
	&& flake8 .\
	&& mypy --strict .

.PHONY = install run debug build clean fclean lint lint-strict
