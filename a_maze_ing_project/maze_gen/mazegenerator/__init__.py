"""This module manages all the classes, enumerations, methods and algorithms
required to generate a maze, within the maze.py file. Several generation
algorithms have been implemented: Backtracking, Prim, Hunt and kill, and
one to made an imperfect maze. We made this choice to highlight the diversity
and complexity of the various existing algorithms. This module contain Maze,
Config, Cell and GenerationError classes, Directions and Movements Enum, and
all functions used to generate a perfect or imperfect maze.
"""

from .maze import (
    Maze, GenerationError,
    MazeDimension, CellCoordinates,
    Directions, Movements)


__all__ = [
    "Maze", "GenerationError",
    "MazeDimension", "CellCoordinates",
    "Directions", "Movements"]
