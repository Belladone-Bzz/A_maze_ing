"""MazeGen module.

Manages all the classes, enumerations, methods and algorithms
required to generate a maze. Several generation
algorithms have been implemented: Backtracking, Prim, Hunt and kill, and
imperfecting algorithms: Choke points and Braided. We made this choice to
highlight the diversity and complexity of the various existing algorithms.
This module contain Maze, Config, Cell and GenerationError classes, Directions
and Movements Enum, and all functions used to generate a perfect or imperfect
maze.

Enables the implementation of a pattern at the center of the Maze, consisting
of closed-off cells declared as such, for aesthetic purposes. Also enables
using the stepped_generation method as a Generator of None to perform
actions each time a meaningful step is done during the generation of the Maze,
for example clearing the terminal and printing the Maze, giving the illusion
of the generation being animated. Otherwise the generate_maze method can be
used to generate it instantly.

An example of execution is present at the bottom of the main file.

#### Classes:
- GenerationError: Raised during the generation of the maze, if any step is
skipped before the next.
- Config: Parameter of the Maze class, taking in all necessary variables to
check them before passing them to the Maze. Inherits BaseModel from Pydantic.
- Maze: Hosts all methods related to its own generation, takes a Config
as argument and duplicates all its attributes.
    - Cell: Nested into Maze, contains a list of walls for each direction
    (booleans) and multiple useful flags.

#### Enums:
- Directions: values 0 to 3 used as an index for the list of wall in the
Cell objects.
- Movements: values sharing names with Directions for code ambivalence,
containing tuples of [int, int] that are either -1, 0 or 1, standing as
the movement to apply to a coordinates to move in one direction or the other.

#### Custom types:
- MazeDimension: int greater than 3
- CellCoordinates: tuple[int, int] where each int is greater than 0

#### Errors raised:
- GenerationError,
- ValidationError,
- IndexError,
- AttributeError.
"""

from .maze import (
    Maze, Config, GenerationError,
    MazeDimension, CellCoordinates,
    Directions, Movements)


__all__ = [
    "Maze", "Config", "GenerationError",
    "MazeDimension", "CellCoordinates",
    "Directions", "Movements"]
