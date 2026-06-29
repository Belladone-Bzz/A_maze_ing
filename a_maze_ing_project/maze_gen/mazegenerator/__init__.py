"""This module manages all the classes, enumerations, methods and algorithms
required to generate a maze, within the maze.py file. Several generation
algorithms have been implemented: Backtracking, Prim, Hunt and kill, and
one to made an imperfect maze. We made this choice to highlight the diversity
and complexity of the various existing algorithms. This module contain Maze,
Config, and Cell classes, Directions and Movements Enum, and all functions used
to generate a perfect or imperfect maze.
"""

from .maze import Maze, MazeDimension, CellCoordinates, Directions, Movements


__all__ = [
    "Maze", "MazeDimension", "CellCoordinates", "Directions", "Movements"]
