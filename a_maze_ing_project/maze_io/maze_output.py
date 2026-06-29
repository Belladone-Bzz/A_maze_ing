
from a_maze_ing_project.maze_gen.mazegenerator import (
    Maze, CellCoordinates, Movements)
from a_maze_ing_project.maze_solve import MazeSolver


def write_out_config(config: dict[str, str]) -> str:
    """Takes a dict of maze information to write out in a file named
    'config.txt'.

    Contains all currently contained variables that can be reparsed and used
    to create a Maze using the a_maze_ing.py program. Includes comments for
    guidance and explanations of each value's purpose.

    Returns a potential error message for file opening issues, or an empty
    string.
    """
    try:
        config_str: str = (
            "# This is the configuration file in which you can enter variable"
            "s, factors and algorithms preferences for your generated maze.\n"
            "\n# Positive numerical values (may exceed terminal maximum "
            f"display size)\n\nWIDTH={config["width"]}\n"
            f"HEIGHT={config["height"]}\n\n"
            "# Positive numerical coordinates separated by a comma (may not "
            f"exceed maze size)\n\nENTRY={config["entry"]}\n"
            f"EXIT={config["exit"]}\n\n"
            "# File to overwrite with hexadecimal maze layout and more\n\n"
            f"OUTPUT_FILE={config["output_file"]}\n\n"
            "# Maze generation factors:\n"
            "# - perfect, for a perfect maze (literally True or False),\n"
            "# - seed, for maze reproducibility (whole number)\n"
            "# - central pattern, to display a predesigned pattern on the "
            "center of the maze,\n"
            "#     Patterns available: Forty_two, Heart, Bee, Bbl, Six_seven, "
            "None\n"
            "# - gen_speed, for generation speed, concerns the displaying of "
            "the maze generating (0 to 10).\n"
            "#     the speed relates to the number of cells added to the maze "
            "between each print, a speed of 0 will skip this display.\n\n"
            f"PERFECT={config["perfect"]}\nSEED={config["seed"]}\n"
            f"PATTERN={config["pattern"]}\n"
            f"GEN_SPEED={config["gen_speed"]}\n\n"
            "# Color, characters and styling theme to apply when printing the "
            "generated maze.\n"
            "#     Themes available: Default, Bee, Metamorphosis, Meuuh, "
            f"Boss_lady\n\nTHEME={config["theme"]}\n\n"
            "# Generation algorithms available: Backtracking, Prim, "
            f"Hunt_and_kill\n\nGEN_ALGORITHM={config["gen_algorithm"]}\n\n"
            "# Solving algorithms available: Breadth_search, Dead_end_filler, "
            f"Dijkstra, A_star\n\nSOL_ALGORITHM={config["sol_algorithm"]}")
        with open("config.txt", 'w') as file:
            print(config_str, end="", file=file)
    except FileNotFoundError:
        return f"- Output file {"config.txt"} not found"
    except PermissionError:
        return f"- Output file {"config.txt"} could not be accessed"
    return ""


def write_out_maze(
        maze: Maze, solver: MazeSolver, config: dict[str, str]) -> str:
    """Takes a Maze object and a config to write out maze's basic
    informations in given output_file (from config dict).

    Writes out cell by cell informations about walls, translating each
    possible direction into binary (0: open way, 1: walled path),
    creating 4 bits bytes for each cell. These are converted into
    hexadecimal, and written out line by line.

    This is followed by entry and exit coordinates, and, letter by letter,
    the shortest found path to resolve the Maze.
    """
    maze_str: str = ""
    for y in range(maze.config.HEIGHT):
        for x in range(maze.config.WIDTH):
            maze_str += hex(int("".join([str(
                int(wall)) for wall in maze.cells[x][y].walls]), 2))[2].upper()
        maze_str += "\n"
    maze_str += f"\n{config["entry"]}\n{config["exit"]}\n"
    path: list[CellCoordinates] = solver.shortest_path
    for index in range(1, len(path)):
        maze_str += Movements((
            path[index][0] - path[index - 1][0],
            path[index][1] - path[index - 1][1])).name[0]
    try:
        with open(config["output_file"], 'w') as file:
            print(maze_str, end="", file=file)
    except FileNotFoundError:
        return f"- Output file {config["output_file"]} not found"
    except PermissionError:
        return f"- Output file {config["output_file"]} could not be accessed"
    return ""
