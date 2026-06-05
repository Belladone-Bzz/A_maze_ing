
from maze_gen import Maze


def write_out_maze(maze: Maze, config: dict[str, str]) -> str:
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
    try:
        with open(config["output_file"], 'w') as file:
            print(maze_str, end="", file=file)
    except FileNotFoundError:
        return f"- Output file {config["output_file"]} not found"
    except PermissionError:
        return f"- Output file {config["output_file"]} could not be accessed"
    return ""
