
from maze_gen import Maze


def write_out_maze(maze: Maze, config: dict[str, str]) -> str:
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
