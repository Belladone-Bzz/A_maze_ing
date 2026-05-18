---

kanban-plugin: board

---

## README

- [ ] - Description
- [ ] Maze generation algorithm (one or multiple) and why
- [ ] Maze solving algorithm (one or multiple)
- [ ] Which part of the code is reusable, how and why
- [ ] Any additional feature
- [ ] - Instruction
- [ ] config.txt syntax
- [ ] Usage of the Makefile and how it works
- [ ] Installation and usage of the included package
- [ ] - Resources
- [ ] AI usage
- [ ] The work management and how it was split between the team
- [ ] How the planned tasks evolved during the project
- [ ] What more could be done or improved
- [ ] The tools and resources used in the making


## Module creation

- [ ] The maze generation must be contained within a single designated class inside a standalone module
- [ ] It must provide a documentation on importing, using and passing custom parameters to the class, as well as how to access the maze structure
- [ ] This module must be built into a package usable and installable by pip, named `mazegen-*` and placed at the root of the repository
- [ ] This file can use the extensions `.tar.gz` and `.whl`


## Makefile

- [ ] Rules:
- [ ] install (`source venv/bin/activate && pip install -r requirements.txt`)
- [ ] run (`source venv/bin/activate && python3 a_maze_ing.py config.txt`)
- [ ] debug (`source venv/bin/activate && debug`)
- [ ] clean (`rm -rf */__pycache__ */mypy_cache`)
- [ ] lint (`flake8 . && mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs`)
- [ ] lint-strict (`flake8 . && mypy --strict .`)


## .gitignore

- [ ] `*/__pycache__`
- [ ] `*/mypy_cache`
- [ ] `*output*`


## Styling

- [ ] All functions must pass mypy and flake8 checks
- [ ] All function parameters, returns and variables must be typed
- [ ] All resources must be read or written in context blocs (`with`)
- [ ] All functions and classes must be documented respecting PEP257


## config.txt

- [ ] Can contain # comment, empty lines and `KEY=VALUE` entries
- [ ] A default configuration must be available on the repository
- [ ] WIDTH: int `0:`
- [ ] HEIGHT: int `0:`
- [ ] ENTRY: tuple[int `0:HEIGHT`, int `0:WIDTH`]
- [ ] EXIT: tuple[int `0:HEIGHT`, int `0:WIDTH`], different from entry
- [ ] OUTPUT_FILE: str
- [ ] PERFECT: bool `False:True`
- [ ] SEED: Any


## Maze

- [ ] Each Cell must contain walls (North, East, South, West)
- [ ] The maze cannot contain open areas larger than 3x2 open spaces (best if every path is 1 cell large)
- [ ] The maze must contain the 42 logo made of fully close cells
- [ ] If the maze is too small to represent the logo, an error message is displayed instead
- [ ] A perfect maze is one where all cells are linked by a single pathway


## Maze visualization

- [ ] The maze can be drawn in terminal using ASCII rendering
- [ ] It must clearly show walls, entry, exit and the found path
- [ ] It must be interactive with at least the following commands:
- [ ] - Regenerate a new maze
- [ ] - Show/hide the shortest path
- [ ] - Change maze wall colors
- [ ] - Change 42 logo colors
- [ ] - Quit


## Output file

- [ ] The output file entered in config.txt must be overwritten with the maze information
- [ ] From the first line, the cells are represented with a hexadecimal value (0:F), with lines separated with a single '\n'
- [ ] Each value stands for a binary code of 4 bits, where 1 stands for a wall, and 0 an open path :
- [ ] 3: West
- [ ] 2: South
- [ ] 1: East
- [ ] 0 (LSB): North
- [ ] WSEN, so 3 (0011) means East and North are closed, or A (1010) means West and East are closed
- [ ] The maze representation is followed by an empty line
- [ ] The entry and exit coordinates are written on each their lines with the syntax: X,Y\n
- [ ] Finally, the shortest found path must be transcribed using the four possible directions WSEN letter by letter, followed by a newline
- [ ] FFFF
	FFFF
	FFFF
	
	0,0
	3,3
	EEESS
	(empty final line)




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false,false,false,false,false]}
```
%%