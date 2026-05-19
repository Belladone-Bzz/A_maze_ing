
from maze_gen import Maze, MazeDimension, CellCoordinates
from sys import argv


if __name__ == "__main__":
    if len(argv) != 2:
        print(
            "Incorrect number of argument;",
            "execute the program using the syntax:\n",
            "python a_maze_ing.py <text file containing maze configuration>")
        exit()
