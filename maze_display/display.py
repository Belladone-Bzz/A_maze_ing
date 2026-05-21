
from .utils import style_print, Theme
from maze_gen import Maze, Directions


def print_maze(maze: Maze, theme: Theme) -> None:

    line: str = str(theme.angles.TOP_LEFT)
    line += "".join(
        str(theme.walls.HORIZONTAL) * 3 + (
            "" if cell.coordinates[0] == maze.config.WIDTH - 1
            else str(theme.walls.HORIZONTAL_D)
            if cell.walls[Directions.EAST] is True
            else str(theme.walls.HORIZONTAL))
        for cell in (maze.cells[x][0] for x in range(maze.config.WIDTH)))
    line += str(theme.angles.TOP_RIGHT)
    style_print(theme.walls_style, line, "\n")

    for y in range(maze.config.HEIGHT):
        line = str(theme.walls.VERTICAL)
        line += "".join(
            "   " + (
                "" if cell.coordinates[0] == maze.config.WIDTH - 1
                else str(theme.walls.VERTICAL)
                if cell.walls[Directions.EAST] is True
                else " ")
            for cell in (maze.cells[x][y] for x in range(maze.config.WIDTH)))
        line += str(theme.walls.VERTICAL)
        style_print(theme.walls_style, line, "\n")

        if y == maze.config.HEIGHT - 1:
            break

        line = (
            str(theme.walls.VERTICAL_R)
            if maze.cells[0][y].walls[Directions.SOUTH] is True
            else str(theme.walls.VERTICAL))
        for x in range(maze.config.WIDTH):
            line += (
                str(theme.walls.HORIZONTAL) * 3
                if maze.cells[x][y].walls[Directions.SOUTH] is True
                else "   ")
            if x == maze.config.WIDTH - 1:
                line += (
                    str(theme.walls.VERTICAL_L)
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    else str(theme.walls.VERTICAL))
                style_print(theme.walls_style, line, "\n")
                continue
            line += (
                str(theme.walls.CROSS)
                if maze.cells[x][y].walls[Directions.SOUTH] is True
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                and maze.cells[x][y].walls[Directions.EAST] is True
                and maze.cells[x][y + 1].walls[Directions.EAST] is True

                else str(theme.walls.VERTICAL)
                if maze.cells[x][y].walls[Directions.SOUTH] is False
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                and (maze.cells[x][y].walls[Directions.EAST] is True
                or maze.cells[x][y + 1].walls[Directions.EAST] is True)

                else str(theme.walls.HORIZONTAL)
                if (maze.cells[x][y].walls[Directions.SOUTH] is True
                or maze.cells[x + 1][y].walls[Directions.SOUTH] is True)
                and maze.cells[x][y].walls[Directions.EAST] is False
                and maze.cells[x][y + 1].walls[Directions.EAST] is False

                else str(theme.walls.VERTICAL_L)
                if maze.cells[x][y].walls[Directions.SOUTH] is True
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                and maze.cells[x][y].walls[Directions.EAST] is True
                and maze.cells[x][y + 1].walls[Directions.EAST] is True

                else str(theme.walls.VERTICAL_R)
                if maze.cells[x][y].walls[Directions.SOUTH] is False
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                and maze.cells[x][y].walls[Directions.EAST] is True
                and maze.cells[x][y + 1].walls[Directions.EAST] is True

                else str(theme.walls.HORIZONTAL_U)
                if maze.cells[x][y].walls[Directions.SOUTH] is True
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                and maze.cells[x][y].walls[Directions.EAST] is True
                and maze.cells[x][y + 1].walls[Directions.EAST] is False

                else str(theme.walls.HORIZONTAL_D)
                if maze.cells[x][y].walls[Directions.SOUTH] is True
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                and maze.cells[x][y].walls[Directions.EAST] is False
                and maze.cells[x][y + 1].walls[Directions.EAST] is True

                else str(theme.angles.TOP_LEFT)
                if maze.cells[x][y].walls[Directions.SOUTH] is False
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                and maze.cells[x][y].walls[Directions.EAST] is False
                and maze.cells[x][y + 1].walls[Directions.EAST] is True

                else str(theme.angles.TOP_RIGHT)
                if maze.cells[x][y].walls[Directions.SOUTH] is True
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                and maze.cells[x][y].walls[Directions.EAST] is False
                and maze.cells[x][y + 1].walls[Directions.EAST] is True

                else str(theme.angles.BOTTOM_LEFT)
                if maze.cells[x][y].walls[Directions.SOUTH] is False
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                and maze.cells[x][y].walls[Directions.EAST] is True
                and maze.cells[x][y + 1].walls[Directions.EAST] is False

                else str(theme.angles.BOTTOM_RIGHT)
                if maze.cells[x][y].walls[Directions.SOUTH] is True
                and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                and maze.cells[x][y].walls[Directions.EAST] is True
                and maze.cells[x][y + 1].walls[Directions.EAST] is False

                else " ")

    line = str(theme.angles.BOTTOM_LEFT)
    line += "".join(
        str(theme.walls.HORIZONTAL) * 3 + (
            "" if cell.coordinates[0] == maze.config.WIDTH - 1
            else str(theme.walls.HORIZONTAL_U)
            if cell.walls[Directions.EAST] is True
            else str(theme.walls.HORIZONTAL))
        for cell in (maze.cells[x][-1] for x in range(maze.config.WIDTH)))
    line += str(theme.angles.BOTTOM_RIGHT)
    style_print(theme.walls_style, line, "\n")
