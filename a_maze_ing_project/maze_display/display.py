
from .utils import style_print, CursorOperations, Shades
from .themes import Theme, get_theme
from a_maze_ing_project.maze_gen import (
    Maze, Directions, Movements, CellCoordinates)
from a_maze_ing_project.maze_solve import MazeSolver
from collections.abc import Callable
from os import get_terminal_size, terminal_size
from time import sleep


def instantiate_maze_display(
        config: dict[str, str]) -> Callable[[str, Maze, MazeSolver], None]:
    """Exposed function of the display file, enclosing all maze-displaying
    functions. Takes a config dict to keep access to updated Maze infos.

    Returns a maze_display function, which takes as arguments an
    action to execute as a string, and a Maze object to display, returning
    None.

    Can:
    "display_maze": display the entire maze after it is generated;
    "display_maze_generation": display the maze at every loop of its
    generation if the terminal is big enough, otherwise generates
    the maze directly;
    "display_maze_solving": display the maze at every loop of its
    solving if the terminal is big enough, otherwise solves
    the maze directly.
    """

    def calculate_intersection_index(
            bin_bool: tuple[bool, bool, bool, bool]) -> int:
        """Returns a decimal value from a 4 bit binary value.

        Uses join and int to first convert the 4 booleans given as parameter
        into binary, then joining them into a string given to int with a base
        of 2 to recover an int between 0 and 15, to be used as an index.
        """
        return int("".join(str(int(bi)) for bi in bin_bool), 2)

    def print_maze(
            maze: Maze, theme: Theme, solver: MazeSolver) -> None:
        """Takes a Maze object to display. Works with utils file, containing
        custom and special characters, as well as Themes, applying
        colors and styling.

        Displays the maze cell by cell, surrounding them with wall
        characters depending on which of their walls are open or not.
        Displays each angle based on open walls, outputting an adaptive
        and clear display.

        Returns None
        """
        print(CursorOperations.MOVE_CURSOR(0, 0))

        path: list[CellCoordinates] = []
        highlight: tuple[CellCoordinates, ...] = ()
        if config["show_path"] == "True":
            path = solver.shortest_path
            highlight = solver.highlighted

        def get_fill_character(
                cell_1: CellCoordinates,
                movement: Movements | None = None) -> str:
            if config["show_path"] == "False":
                return " "
            cell_2: CellCoordinates
            fill: tuple[str, str, str] = (
                theme.visited_style + Shades.LIGHT_SHADE.value,
                theme.highlighted_style + Shades.DARK_SHADE.value,
                theme.path_style + Shades.MEDIUM_SHADE.value)
            if movement is not None:
                if maze.cells[cell_1[0]][cell_1[1]].walls[
                        Directions[movement.name]] is True:
                    return " "
                cell_2 = maze.get_neighbor_coords(
                    cell_1, movement.value)
            else:
                cell_2 = cell_1
            return (
                fill[2] if (cell_1 in path and cell_2 in path)
                else fill[1] if (cell_1 in highlight and cell_2 in highlight)
                else fill[0] if (
                    maze.cells[cell_1[0]][cell_1[1]].is_visited is True
                    and maze.cells[cell_2[0]][cell_2[1]].is_visited is True
                    and (
                        cell_1 == cell_2
                        or solver.algorithm not in ("Dijkstra", "A_star")))
                else " ") + theme.walls_style

        line: str = str(theme.angles.TOP_LEFT)
        line += "".join(
            str(theme.walls.HORIZONTAL) * 3 + (
                "" if cell.coordinates[0] == maze.config.WIDTH - 1
                else str(theme.walls.HORIZONTAL_D)
                if cell.walls[Directions.EAST] is True
                else str(theme.walls.HORIZONTAL))
            for cell in (maze.cells[x][0] for x in range(maze.config.WIDTH)))
        line += str(theme.angles.TOP_RIGHT)
        style_print(
            theme.walls_style, line,
            f"{CursorOperations.LIGHT_LINE_CLEAR}\n")

        intersections: tuple[str, ...] = (
            str(theme.walls.DOT),
            str(theme.walls.VERTICAL),
            str(theme.walls.VERTICAL),
            str(theme.walls.VERTICAL),
            str(theme.walls.HORIZONTAL),
            str(theme.angles.TOP_LEFT),
            str(theme.angles.BOTTOM_LEFT),
            str(theme.walls.VERTICAL_R),
            str(theme.walls.HORIZONTAL),
            str(theme.angles.TOP_RIGHT),
            str(theme.angles.BOTTOM_RIGHT),
            str(theme.walls.VERTICAL_L),
            str(theme.walls.HORIZONTAL),
            str(theme.walls.HORIZONTAL_D),
            str(theme.walls.HORIZONTAL_U),
            str(theme.walls.CROSS))

        for y in range(maze.config.HEIGHT):
            line = str(theme.walls.VERTICAL)
            for x in range(maze.config.WIDTH):
                line += get_fill_character((x, y), Movements.WEST)
                line += get_fill_character((x, y))
                line += get_fill_character((x, y), Movements.EAST)
                line += (
                    str(theme.walls.VERTICAL)
                    if maze.cells[x][y].walls[Directions.EAST] is True
                    else get_fill_character((x, y), Movements.EAST))
            style_print(
                theme.walls_style, line,
                f"{CursorOperations.LIGHT_LINE_CLEAR}\n")

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
                    else (
                        " " + get_fill_character((x, y), Movements.SOUTH)
                        + " "))
                if x == maze.config.WIDTH - 1:
                    line += (
                        str(theme.walls.VERTICAL_L)
                        if maze.cells[x][y].walls[Directions.SOUTH] is True
                        else str(theme.walls.VERTICAL))
                    style_print(
                        theme.walls_style, line,
                        f"{CursorOperations.LIGHT_LINE_CLEAR}\n")
                    break
                line += intersections[calculate_intersection_index((
                    maze.cells[x][y].walls[Directions.SOUTH],
                    maze.cells[x + 1][y].walls[Directions.SOUTH],
                    maze.cells[x][y].walls[Directions.EAST],
                    maze.cells[x][y + 1].walls[Directions.EAST]))]

        line = str(theme.angles.BOTTOM_LEFT)
        line += "".join(
            str(theme.walls.HORIZONTAL) * 3 + (
                str(theme.angles.BOTTOM_RIGHT)
                if cell.coordinates[0] == maze.config.WIDTH - 1
                else str(theme.walls.HORIZONTAL_U)
                if cell.walls[Directions.EAST] is True
                else str(theme.walls.HORIZONTAL))
            for cell in (maze.cells[x][-1] for x in range(maze.config.WIDTH)))
        style_print(theme.walls_style, line, "\n")

    def integrate_entry_exit(maze: Maze, theme: Theme) -> None:
        """Function called after print_maze, going back on the print to
        integrate the icons for the entry and the exit coordinates with
        their corresponding styling.

        Returns None
        """
        print(CursorOperations.SAVE_CURSOR, end="")
        for coords, style, icon in zip(
                (maze.config.ENTRY, maze.config.EXIT),
                (theme.start_style, theme.exit_style),
                (theme.start, theme.exit)):
            style_print(style, CursorOperations.MOVE_CURSOR(
                coords[1] * 2 + 3, coords[0] * 4 + 3) + str(icon))
        print(CursorOperations.LOAD_CURSOR, end="")

    def integrate_pattern_design(maze: Maze, theme: Theme) -> None:
        """Function called after print_maze, going back on the print to
        integrate the selected pattern design. Works with Patterns enum,
        and takes a Maze object as parameter.

        Prints out the central pattern adapatively, checking line by line
        which angle or interception should be printed out.

        Returns None
        """
        intersections: tuple[str, ...] = (
            str(CursorOperations.MOVE_RIGHT),
            str(theme.icon_angles.BOTTOM_RIGHT),
            str(theme.icon_angles.BOTTOM_LEFT),
            str(theme.icon_walls.HORIZONTAL_U),
            str(theme.icon_angles.TOP_RIGHT),
            str(theme.icon_walls.VERTICAL_L),
            str(theme.icon_walls.CROSS),
            str(theme.icon_walls.CROSS),
            str(theme.icon_angles.TOP_LEFT),
            str(theme.icon_walls.CROSS),
            str(theme.icon_walls.VERTICAL_R),
            str(theme.icon_walls.CROSS),
            str(theme.icon_walls.HORIZONTAL_D),
            str(theme.icon_walls.CROSS),
            str(theme.icon_walls.CROSS),
            str(theme.icon_walls.CROSS))
        pattern: list[list[bool]] = maze.config.PATTERN
        lines: str = ""

        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                lines += intersections[calculate_intersection_index((
                    pattern[y][x],
                    False if x == 0 else pattern[y][x - 1],
                    False if y == 0 else pattern[y - 1][x],
                    False if x == 0 or y == 0 else pattern[y - 1][x - 1]))]
                lines += (
                    theme.icon_walls.HORIZONTAL * 3
                    if pattern[y][x] is True or (
                        y != 0 and pattern[y - 1][x] is True)
                    else str(CursorOperations.MOVE_RIGHT) * 3)
            lines += intersections[calculate_intersection_index((
                    False,
                    pattern[y][x],
                    False,
                    False if y == 0 else pattern[y - 1][x]))] + "\n"
            for x in range(len(pattern[0])):
                if pattern[y][x] is True:
                    lines += (
                        theme.icon_walls.VERTICAL
                        + theme.icon_content)
                else:
                    lines += (
                        theme.icon_walls.VERTICAL
                        if x != 0 and pattern[y][x - 1] is True
                        else str(CursorOperations.MOVE_RIGHT))
                    lines += str(CursorOperations.MOVE_RIGHT) * 3
            lines += (
                theme.icon_walls.VERTICAL
                if pattern[y][x] is True
                else str(CursorOperations.MOVE_RIGHT)) + "\n"
        for x in range(len(pattern[0])):
            lines += intersections[calculate_intersection_index((
                    False,
                    False,
                    pattern[y][x],
                    False if x == 0 else pattern[y][x - 1]))]
            lines += (
                theme.icon_walls.HORIZONTAL * 3
                if pattern[y][x] is True else
                str(CursorOperations.MOVE_RIGHT) * 3)
        lines += (
            theme.icon_angles.BOTTOM_RIGHT
            if pattern[y][-1] is True
            else str(CursorOperations.MOVE_RIGHT)
        )
        print(CursorOperations.SAVE_CURSOR, end="")
        for index, line in enumerate(lines.split("\n")):
            print(CursorOperations.MOVE_CURSOR(
                (maze.pattern_v_offset * 2 + index + 2),
                maze.pattern_h_offset * 4 + 1), end="")
            style_print(theme.icon_style, line)
        print(CursorOperations.LOAD_CURSOR, end="")

    def integrate_found_path(
            theme: Theme, path: list[CellCoordinates]) -> None:
        """Function called after print_maze, going back on the print to
        integrate the solver's found path. Works with nested functions
        get_line_character and add_cell_separation to integrate the selected
        theme's characters and styling for the path.

        Returns None
        """
        if len(path) < 3:
            return

        def get_line_character(index: int) -> str:
            """Returns a special character corresponding to the trajectory of
            the path through the cell situated at the given index. Doesn't
            support entry and exit point as they are represented by their own
            character. Calculate both the movement from the last cell and to
            the next to chose which character to return, from the selected
            theme's path_chars attribute.
            """
            cell_0: CellCoordinates = path[index - 1]
            cell_1: CellCoordinates = path[index]
            cell_2: CellCoordinates = path[index + 1]
            back: int = Directions[Movements(
                (cell_1[0] - cell_0[0], cell_1[1] - cell_0[1])).name].value
            front: int = Directions[Movements(
                (cell_1[0] - cell_2[0], cell_1[1] - cell_2[1])).name].value
            match sorted((back, front)):
                case (Directions.SOUTH.value, Directions.NORTH.value):
                    return theme.path_chars[0].VERTICAL
                case (Directions.WEST.value, Directions.EAST.value):
                    return theme.path_chars[0].HORIZONTAL
                case (Directions.EAST.value, Directions.NORTH.value):
                    return theme.path_chars[1].TOP_RIGHT
                case (Directions.SOUTH.value, Directions.EAST.value):
                    return theme.path_chars[1].BOTTOM_RIGHT
                case (Directions.WEST.value, Directions.NORTH.value):
                    return theme.path_chars[1].TOP_LEFT
                case (Directions.WEST.value, Directions.SOUTH.value):
                    return theme.path_chars[1].BOTTOM_LEFT
                case _:
                    return " "

        def add_cell_separation(
                line: str, index: int, cell: CellCoordinates) -> str:
            """Appends to the path string special characters to print where
            cells meet, between the path's angles. Takes a cell and its index
            to find out where to place the cursor and what character to print
            based on the direction to take between the current cell and the
            next.
            """
            if path[index + 1][0] < cell[0]:
                line += CursorOperations.MOVE_CURSOR(
                    cell[1] * 2 + 3, cell[0] * 4)
                line += theme.path_chars[0].HORIZONTAL * 3
            elif path[index + 1][0] > cell[0]:
                line += CursorOperations.MOVE_CURSOR(
                    cell[1] * 2 + 3, cell[0] * 4 + 4)
                line += theme.path_chars[0].HORIZONTAL * 3
            elif path[index + 1][1] < cell[1]:
                line += CursorOperations.MOVE_CURSOR(
                    cell[1] * 2 + 2, cell[0] * 4 + 3)
                line += theme.path_chars[0].VERTICAL
            elif path[index + 1][1] > cell[1]:
                line += CursorOperations.MOVE_CURSOR(
                    cell[1] * 2 + 4, cell[0] * 4 + 3)
                line += theme.path_chars[0].VERTICAL
            return line

        line: str = add_cell_separation("", 0, path[0])
        for index, cell in enumerate(path[1:-1], 1):
            line += CursorOperations.MOVE_CURSOR(
                cell[1] * 2 + 3, cell[0] * 4 + 3) + get_line_character(index)
            line = add_cell_separation(line, index, cell)
        print(CursorOperations.SAVE_CURSOR, end="")
        style_print(theme.path_style, line)
        print(CursorOperations.LOAD_CURSOR, end="")

    def display_maze_generation(
            maze: Maze, theme: Theme, solver: MazeSolver) -> None:
        """Function called to trigger the given Maze's generation using its
        Generator method to call print_maze every time a new cell is
        accessed. Also checks the terminal window size using termios
        to only trigger the generation and not display it if it's too
        small.

        Returns None
        """
        print(CursorOperations.HEAVY_CLEAR, end="")
        window_size: terminal_size = get_terminal_size()
        if (
                maze.config.WIDTH * 4 < window_size.columns
                and maze.config.HEIGHT * 2 < window_size.lines
                and int(config["gen_speed"]) != 0):
            step: int = 0
            for _ in maze.stepped_generation():
                if step % int(config["gen_speed"]) == 0:
                    print_maze(maze, theme, solver)
                sleep(0.004)
                step += 1
        else:
            maze.generate_maze()

    def display_maze_solving(
            maze: Maze, theme: Theme, solver: MazeSolver) -> None:
        """Function called to trigger the given Maze's solving using the
        given MazeSolver object to call print_maze everytime the chosen
        algorithm yields None. Also checks the terminal window size using
        termios to only trigger the generation and not display it if it's too
        small.

        Returns None
        """
        print(CursorOperations.HEAVY_CLEAR, end="")
        window_size: terminal_size = get_terminal_size()

        if (
                maze.config.WIDTH * 4 < window_size.columns
                and maze.config.HEIGHT * 2 < window_size.lines
                and int(config["gen_speed"]) != 0):
            step: int = 0
            for _ in solver.stepped_maze_solving():
                if step % int(config["gen_speed"]) == 0:
                    print_maze(maze, theme, solver)
                sleep(0.004)
                step += 1
        else:
            solver.maze_solving()

    def display_maze(maze: Maze, theme: Theme, solver: MazeSolver) -> None:
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
            print_maze(maze, theme, solver)
            if maze.config.PATTERN != []:
                integrate_pattern_design(maze, theme)
            if config["show_path"] == "True":
                integrate_found_path(theme, solver.shortest_path)
            integrate_entry_exit(maze, theme)
        else:
            print(CursorOperations.MOVE_CURSOR(0, 0))
            style_print(
                theme.walls_style,
                "\nThe window is too small to show the Maze.".center(41),
                end="\n")
            style_print(
                theme.walls_style,
                "Save it to an output file or increase the".center(41),
                end="\n")
            style_print(
                theme.walls_style,
                "window's size to preview it.".center(41),
                end="\n\n")

    def maze_display(
            current_display: str, maze: Maze, solver: MazeSolver) -> None:
        """Function returned by instantiate_maze_display to give access to all
        enclosed functions. Takes an action as a string and a Maze object
        to display either generating or generated, applying a Theme
        using the current configuration.

        Returns None
        """
        current_theme = get_theme(config["theme"])
        if current_display == "display_maze":
            display_maze(maze, current_theme, solver)
        elif current_display == "display_maze_generation":
            display_maze_generation(maze, current_theme, solver)
        elif current_display == "display_maze_solving":
            display_maze_solving(maze, current_theme, solver)

    return maze_display
