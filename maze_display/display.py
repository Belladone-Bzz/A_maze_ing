
from .utils import style_print, CursorOperations, SmallIcons, move_cursor
from .themes import Theme, get_theme
from maze_gen import Maze, Directions
from collections.abc import Callable
from os import get_terminal_size, terminal_size
from time import sleep


def instantiate_maze_display(
        config: dict[str, str]) -> Callable[[str, Maze], None]:
    """Exposed function of the display file, enclosing all maze-displaying
    functions. Takes a config dict to keep access to updated Maze infos.

    Returns a maze_display function, which takes as arguments an
    action to execute as a string, and a Maze object to display, returning
    None.

    Can:
    "display_maze": display the entire maze after it is generated;
    "display_maze_generation": display the maze at every loop of its
    generation if the terminal is big enough, otherwise generates
    the maze  directly.
    """

    current_theme: Theme = get_theme(config["theme"])

    def print_maze(maze: Maze) -> None:
        """Takes a Maze object to display. Works with utils file, containing
        custom and special characters, as well as Themes, applying
        colors and styling.

        Displays the maze cell by cell, surrounding them with wall
        characters depending on which of their walls are open or not.
        Displays each angle based on open walls, outputting an adaptive
        and clear display.

        Returns None
        """
        print(move_cursor(0, 0))

        emojis: tuple[SmallIcons, ...] = (
            SmallIcons.COOKIE, SmallIcons.BEE, SmallIcons.FLOWER,
            SmallIcons.BUTTERFLY, SmallIcons.CATERPILLAR, SmallIcons.COW,
            SmallIcons.MILK, SmallIcons.TONGUE, SmallIcons.BIKINI)

        line: str = str(current_theme.angles.TOP_LEFT)
        line += "".join(
            str(current_theme.walls.HORIZONTAL) * 3 + (
                "" if cell.coordinates[0] == maze.config.WIDTH - 1
                else str(current_theme.walls.HORIZONTAL_D)
                if cell.walls[Directions.EAST] is True
                else str(current_theme.walls.HORIZONTAL))
            for cell in (maze.cells[x][0] for x in range(maze.config.WIDTH)))
        line += str(current_theme.angles.TOP_RIGHT)
        style_print(
            current_theme.walls_style, line,
            f"{CursorOperations.LIGHT_LINE_CLEAR}\n")

        for y in range(maze.config.HEIGHT):
            line = str(current_theme.walls.VERTICAL)
            for x in range(maze.config.WIDTH):
                if maze.cells[x][y].entry is True:
                    line += (
                        f" {current_theme.start_style}{current_theme.start}"
                        f"{current_theme.walls_style} "
                        if current_theme.start not in emojis
                        else f" {current_theme.start}")
                elif maze.cells[x][y].exit is True:
                    line += (
                        f" {current_theme.exit_style}{current_theme.exit}"
                        f"{current_theme.walls_style} "
                        if current_theme.exit not in emojis
                        else f" {current_theme.exit}")
                else:
                    line += "   "
                if x == maze.config.WIDTH - 1:
                    break
                line += (
                        str(current_theme.walls.VERTICAL)
                        if maze.cells[x][y].walls[Directions.EAST] is True
                        else " ")
            line += str(current_theme.walls.VERTICAL)
            style_print(
                current_theme.walls_style, line,
                f"{CursorOperations.LIGHT_LINE_CLEAR}\n")

            if y == maze.config.HEIGHT - 1:
                break

            line = (
                str(current_theme.walls.VERTICAL_R)
                if maze.cells[0][y].walls[Directions.SOUTH] is True
                else str(current_theme.walls.VERTICAL))
            for x in range(maze.config.WIDTH):
                line += (
                    str(current_theme.walls.HORIZONTAL) * 3
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    else "   ")
                if x == maze.config.WIDTH - 1:
                    line += (
                        str(current_theme.walls.VERTICAL_L)
                        if maze.cells[x][y].walls[Directions.SOUTH] is True
                        else str(current_theme.walls.VERTICAL))
                    style_print(
                        current_theme.walls_style, line,
                        f"{CursorOperations.LIGHT_LINE_CLEAR}\n")
                    continue
                line += (
                    str(current_theme.walls.CROSS)
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                    and maze.cells[x][y].walls[Directions.EAST] is True
                    and maze.cells[x][y + 1].walls[Directions.EAST] is True

                    else str(current_theme.walls.VERTICAL)
                    if maze.cells[x][y].walls[Directions.SOUTH] is False
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                    and (
                        maze.cells[x][y].walls[Directions.EAST] is True
                        or maze.cells[x][y + 1].walls[Directions.EAST] is True)

                    else str(current_theme.walls.HORIZONTAL)
                    if (
                        maze.cells[x][y].walls[Directions.SOUTH] is True
                        or maze.cells[x + 1][y].walls[Directions.SOUTH]
                        is True)
                    and maze.cells[x][y].walls[Directions.EAST] is False
                    and maze.cells[x][y + 1].walls[Directions.EAST] is False

                    else str(current_theme.walls.VERTICAL_L)
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                    and maze.cells[x][y].walls[Directions.EAST] is True
                    and maze.cells[x][y + 1].walls[Directions.EAST] is True

                    else str(current_theme.walls.VERTICAL_R)
                    if maze.cells[x][y].walls[Directions.SOUTH] is False
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                    and maze.cells[x][y].walls[Directions.EAST] is True
                    and maze.cells[x][y + 1].walls[Directions.EAST] is True

                    else str(current_theme.walls.HORIZONTAL_U)
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                    and maze.cells[x][y].walls[Directions.EAST] is True
                    and maze.cells[x][y + 1].walls[Directions.EAST] is False

                    else str(current_theme.walls.HORIZONTAL_D)
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                    and maze.cells[x][y].walls[Directions.EAST] is False
                    and maze.cells[x][y + 1].walls[Directions.EAST] is True

                    else str(current_theme.angles.TOP_LEFT)
                    if maze.cells[x][y].walls[Directions.SOUTH] is False
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                    and maze.cells[x][y].walls[Directions.EAST] is False
                    and maze.cells[x][y + 1].walls[Directions.EAST] is True

                    else str(current_theme.angles.TOP_RIGHT)
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                    and maze.cells[x][y].walls[Directions.EAST] is False
                    and maze.cells[x][y + 1].walls[Directions.EAST] is True

                    else str(current_theme.angles.BOTTOM_LEFT)
                    if maze.cells[x][y].walls[Directions.SOUTH] is False
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is True
                    and maze.cells[x][y].walls[Directions.EAST] is True
                    and maze.cells[x][y + 1].walls[Directions.EAST] is False

                    else str(current_theme.angles.BOTTOM_RIGHT)
                    if maze.cells[x][y].walls[Directions.SOUTH] is True
                    and maze.cells[x + 1][y].walls[Directions.SOUTH] is False
                    and maze.cells[x][y].walls[Directions.EAST] is True
                    and maze.cells[x][y + 1].walls[Directions.EAST] is False

                    else " ")

        line = str(current_theme.angles.BOTTOM_LEFT)
        line += "".join(
            str(current_theme.walls.HORIZONTAL) * 3 + (
                "" if cell.coordinates[0] == maze.config.WIDTH - 1
                else str(current_theme.walls.HORIZONTAL_U)
                if cell.walls[Directions.EAST] is True
                else str(current_theme.walls.HORIZONTAL))
            for cell in (maze.cells[x][-1] for x in range(maze.config.WIDTH)))
        line += str(current_theme.angles.BOTTOM_RIGHT)
        style_print(current_theme.walls_style, line, "\n")

    def integrate_pattern_design(maze: Maze) -> None:
        """Function called after print_maze, going back on the print to
        integrate the selected pattern design. Works with Patterns enum,
        and takes a Maze object as parameter.

        Prints out the central pattern adapatively, checking line by line
        which angle or interception should be printed out.

        Returns None
        """
        pattern: list[list[bool]] = maze.config.PATTERN
        lines: str = ""
        horizontal_offset: int = (
            int(maze.config.WIDTH / 2)
            - int(len(pattern[0]) / 2))
        vertical_offset: int = (
            int(maze.config.HEIGHT / 2)
            - int(len(pattern) / 2))

        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                if pattern[y][x] is True:
                    lines += (
                        current_theme.icon_angles.TOP_LEFT
                        if (x == 0 and y == 0)
                        or (x == 0 and pattern[y - 1][x] is False)
                        or (y == 0 and pattern[y][x - 1] is False)
                        or (
                            x != 0 and y != 0
                            and pattern[y - 1][x - 1] is False
                            and pattern[y - 1][x] is False
                            and pattern[y][x - 1] is False)
                        else current_theme.icon_walls.HORIZONTAL_D
                        if x != 0 and pattern[y][x - 1] is True and (
                            y == 0 or (
                                pattern[y - 1][x - 1] is False
                                and pattern[y - 1][x] is False))
                        else current_theme.icon_walls.VERTICAL_R
                        if y != 0 and pattern[y - 1][x] is True and (
                            x == 0 or (
                                pattern[y - 1][x - 1] is False
                                and pattern[y][x - 1] is False))
                        else current_theme.icon_walls.CROSS)
                    lines += current_theme.icon_walls.HORIZONTAL * 3
                else:
                    lines += (
                        current_theme.icon_angles.TOP_RIGHT
                        if x != 0 and pattern[y][x - 1] is True and (
                            y == 0 or (
                                pattern[y - 1][x] is False
                                and pattern[y - 1][x - 1] is False))
                        else current_theme.icon_angles.BOTTOM_LEFT
                        if y != 0 and pattern[y - 1][x] is True and (
                            x == 0 or (
                                pattern[y][x - 1] is False
                                and pattern[y - 1][x - 1] is False))
                        else current_theme.icon_angles.BOTTOM_RIGHT
                        if y != 0 and x != 0
                        and pattern[y][x - 1] is False
                        and pattern[y - 1][x] is False
                        and pattern[y - 1][x - 1] is True
                        else current_theme.icon_walls.HORIZONTAL_U
                        if y != 0 and x != 0
                        and pattern[y][x - 1] is False
                        and pattern[y - 1][x] is True
                        and pattern[y - 1][x - 1] is True
                        else current_theme.icon_walls.VERTICAL_L
                        if y != 0 and x != 0
                        and pattern[y][x - 1] is True
                        and pattern[y - 1][x] is False
                        and pattern[y - 1][x - 1] is True
                        else current_theme.icon_walls.CROSS
                        if y != 0 and x != 0
                        and pattern[y][x - 1] is True
                        and pattern[y - 1][x] is True
                        else str(CursorOperations.MOVE_RIGHT))
                    lines += (
                        str(CursorOperations.MOVE_RIGHT) * 3
                        if y == 0 or pattern[y - 1][x] is False
                        else current_theme.icon_walls.HORIZONTAL * 3)
                if x == len(pattern[0]) - 1:
                    lines += (
                        current_theme.icon_angles.TOP_RIGHT
                        if pattern[y][x] is True and (
                            y == 0 or pattern[y - 1][x] is False)
                        else current_theme.icon_walls.VERTICAL_L
                        if pattern[y][x] is True and y != 0
                        and pattern[y - 1][x] is True
                        else current_theme.icon_angles.BOTTOM_RIGHT
                        if pattern[y][x] is False and y != 0
                        and pattern[y - 1][x] is True
                        else str(CursorOperations.MOVE_RIGHT)
                    ) + "\n"
            for x in range(len(pattern[0])):
                if pattern[y][x] is True:
                    lines += (
                        current_theme.icon_walls.VERTICAL
                        + current_theme.icon_content)
                else:
                    lines += (
                        current_theme.icon_walls.VERTICAL
                        if x != 0 and pattern[y][x - 1] is True
                        else str(CursorOperations.MOVE_RIGHT))
                    lines += str(CursorOperations.MOVE_RIGHT) * 3
                if x == len(pattern[0]) - 1:
                    lines += (
                        current_theme.icon_walls.VERTICAL
                        if pattern[y][x] is True
                        else str(CursorOperations.MOVE_RIGHT)) + "\n"
            if y == len(pattern) - 1:
                for x in range(len(pattern[0])):
                    lines += (
                        current_theme.icon_angles.BOTTOM_LEFT
                        if pattern[y][x] is True and (
                            x == 0 or pattern[y][x - 1] is False)
                        else current_theme.icon_walls.HORIZONTAL_U
                        if pattern[y][x] is True
                        and x != 0 and pattern[y][x - 1] is True
                        else current_theme.icon_angles.BOTTOM_RIGHT
                        if pattern[y][x] is False
                        and x != 0 and pattern[y][x - 1] is True
                        else str(CursorOperations.MOVE_RIGHT))
                    lines += (
                        current_theme.icon_walls.HORIZONTAL * 3
                        if pattern[y][x] is True else
                        str(CursorOperations.MOVE_RIGHT) * 3)
                lines += (
                    current_theme.icon_angles.BOTTOM_RIGHT
                    if pattern[y][len(pattern[0]) - 1] is True
                    else str(CursorOperations.MOVE_RIGHT)
                )
        print(CursorOperations.SAVE_CURSOR, end="")
        for index, line in enumerate(lines.split("\n")):
            print(CursorOperations.MOVE_CURSOR(
                (vertical_offset * 2 + index + 2),
                horizontal_offset * 4 + 1), end="")
            style_print(current_theme.icon_style, line)
        print(CursorOperations.LOAD_CURSOR, end="")

    def display_maze(maze: Maze) -> None:
        """Function called to display the Maze given as argument.

        Checks the size of the terminal session using termios and either
        displays the full by calling print_maze function, or a custom
        message.

        Returns None
        """
        window_size: terminal_size = get_terminal_size()
        if (
                maze.config.WIDTH * 4 < window_size.columns
                and maze.config.HEIGHT * 2 < window_size.lines):
            print_maze(maze)
            integrate_pattern_design(maze)
        else:
            style_print(
                current_theme.walls_style,
                "The window is too small to display the Maze.\n"
                "Save it to an output file or increase the window's size to "
                "preview it.")

    def display_maze_generation(maze: Maze) -> None:
        """Function called to trigger the given Maze's generation using its
        Generator method to call print_maze every time a new cell is
        accessed. Also checks the terminal window size using termios
        to only trigger the generation and not display it.

        Returns None
        """
        print(CursorOperations.HEAVY_CLEAR, end="")
        window_size: terminal_size = get_terminal_size()
        if (
                maze.config.WIDTH * 4 < window_size.columns
                and maze.config.HEIGHT * 2 < window_size.lines):
            for _ in maze.stepped_generation():
                print_maze(maze)
                integrate_pattern_design(maze)
                sleep(0.005)
        else:
            maze.generate_maze()

    prints: dict[str, Callable[[Maze], None]] = {
        "display_maze": display_maze,
        "display_maze_generation": display_maze_generation}

    def maze_display(current_display: str, maze: Maze) -> None:
        """Function returned by instantiate_maze_display to give access to all
        enclosed functions. Takes an action as a string and a Maze object
        to display either generating or generated, applying a Theme
        using the current configuration.

        Returns None
        """
        nonlocal current_theme
        current_theme = get_theme(config["theme"])
        prints.get(current_display, display_maze)(maze)

    return maze_display
