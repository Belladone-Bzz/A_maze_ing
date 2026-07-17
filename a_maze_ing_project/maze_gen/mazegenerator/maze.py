"""This module manages all the classes, enumerations, methods and algorithms
required to generate a maze, within the maze.py file. Several generation
algorithms have been implemented: Backtracking, Prim, Hunt and kill, and
one to made an imperfect maze. We made this choice to highlight the diversity
and complexity of the various existing algorithms. This module contain Maze,
Config, Cell and GenerationError classes, Directions and Movements Enum, and
all functions used to generate a perfect or imperfect maze.
"""

from pydantic import BaseModel, Field, model_validator
from typing import Annotated
from collections.abc import Generator, Callable
from enum import IntEnum, Enum
from random import seed as set_seed, choice, randint, shuffle


MazeDimension = Annotated[int, Field(ge=3)]
CellCoordinates = Annotated[
    tuple[
        Annotated[int, Field(ge=0)],
        Annotated[int, Field(ge=0)]],
    Field(min_length=2, max_length=2)]


class GenerationError(Exception):
    """Custom exception raised at specific times if the maze generation steps
    have not been correctly called, which would result in unexpected errors.

    Otherwise raised in the single case scenario where the entry or
    exit coordinates are stuck inside the central pattern.

    #### Parameters:
    - Maze object that has raised the error (to print with str or repr method)
    - msg, a string message containing a specialized notice on the exception
    that occured
    """
    def __init__(self, maze: 'Maze', msg: str) -> None:
        self.maze = maze
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class Directions(IntEnum):
    """Class Directions.
    Enum for west(0), south(1), east(2), north(3).
    """
    WEST = 0
    SOUTH = 1
    EAST = 2
    NORTH = 3


class Movements(Enum):
    """Class Movements.
    Enum for:
    - west(-1, 0),
    - south(0, +1),
    - east(+1, 0),
    - north(0, -1).

    Each direction is associated with
    a tuple of x, y movements to go on in the given direction.
    """
    WEST = (-1, 0)
    SOUTH = (0, +1)
    EAST = (+1, 0)
    NORTH = (0, -1)


class Config(BaseModel):
    """Class Config
    Attributes: WIDTH, HEIGHT, ENTRY, EXIT, GEN_ALGORITHM
    IMPERFECT_ALGORITHM, PATTERN, PERFECT, SEED.
    Methods: validate_config.
    """
    WIDTH: MazeDimension
    HEIGHT: MazeDimension
    ENTRY: CellCoordinates
    EXIT: CellCoordinates

    GEN_ALGORITHM: Annotated[str, Field(min_length=1, max_length=15)]
    IMPERFECT_ALGORITHM: Annotated[str, Field(min_length=1, max_length=15)]

    PATTERN: Annotated[list[list[bool]], Field(default=[])]
    PERFECT: Annotated[bool, Field()]
    SEED: Annotated[int, Field()]

    def check_pattern(self) -> str:
        """Run every test related to pattern validation:
        - Check if every line and column is the same length,
        - Check if the pattern is taller or wider than the maze,
        - Check if the entry or exit coordinates are on a True value of the
        pattern.

        Returns an error message if any check encounter an error, else an empty
        string.
        """
        message: str = ""
        if self.PATTERN == []:
            return ""
        if all(len(line) == len(self.PATTERN[0])
                for line in self.PATTERN) is False:
            message += (
                "The integrated pattern must be a tuple of tuple containing "
                "boolean values only, with each line being the same length.")
        if (self.WIDTH < len(self.PATTERN[0]) + 2
                or self.HEIGHT < len(self.PATTERN) + 2):
            message += (
                "Generating a maze when integrating the central "
                "pattern must be done with appropriate dimensions.")
        h_offset: int = (int(self.WIDTH / 2) - int(len(self.PATTERN[0]) / 2))
        v_offset: int = (int(self.HEIGHT / 2) - int(len(self.PATTERN) / 2))
        h_range: range = range(h_offset, h_offset + len(self.PATTERN[0]))
        v_range: range = range(v_offset, v_offset + len(self.PATTERN))
        if (self.ENTRY[0] in h_range and self.ENTRY[1] in v_range
                and self.PATTERN[self.ENTRY[1] - v_offset]
                [self.ENTRY[0] - h_offset] is True):
            message += ("Entry coordinates cannot be placed in pattern cells.")
        if (self.EXIT[0] in h_range and self.EXIT[1] in v_range
                and self.PATTERN[self.EXIT[1] - v_offset]
                [self.EXIT[0] - h_offset] is True):
            message += ("Exit coordinates cannot be placed in pattern cells.")
        return message

    @model_validator(mode='after')
    def validate_config(self) -> "Config":
        """Model validator for maze's configuration, run these verifications:
        - Check the generation and imperfect algorithms provided are
        implemented in the Maze class,
        - Check if the entry and exit coordinates are different and in range
        of the maze,
        - Run the check_pattern method with all pattern related validations.

        Returns an error message made of every error encountered, otherwise
        an empty string.
        """
        error_message: str = ""
        if self.GEN_ALGORITHM not in Maze.generation_algorithms:
            error_message += (
                f"Invalid generation algorithm entered:"
                f"{self.GEN_ALGORITHM}. "
                f"Available: {", ".join(Maze.generation_algorithms)}")
        if self.IMPERFECT_ALGORITHM not in Maze.imperfect_algorithms:
            error_message += (
                f"Invalid imperfect maze generation algorithm entered:"
                f"{self.IMPERFECT_ALGORITHM}. "
                f"Available: {", ".join(Maze.imperfect_algorithms)}")
        if self.ENTRY == self.EXIT:
            error_message += (
                "Entry and exit coordinates cannot be "
                "on the same position.")
        if self.ENTRY[0] >= self.WIDTH or self.ENTRY[1] >= self.HEIGHT:
            error_message += (
                "Entry coordinates (x, y) "
                "cannot exceed the maze's dimensions.")
        if self.EXIT[0] >= self.WIDTH or self.EXIT[1] >= self.HEIGHT:
            error_message += (
                "Exit coordinates (x, y) "
                "cannot exceed the maze's dimensions.")
        error_message += self.check_pattern()
        if error_message != "":
            raise ValueError(error_message)
        return self


class Maze:
    """### Class Maze.
    Nested class: Cell.

    #### Parameter:
    - Config object

    #### Attributes:
    - From Config object:
        - width, height, entry, exit, perfect,
        - gen_algorithm, imperfect_algorithm,
        - seed, pattern.
    - From Maze itself:
        - cells,
        - pattern_width, pattern_height, pattern_h_offset, pattern_v_offset,
        - initialized, generated, imperfected, pattern_implemented.

    #### Methods:
    - init, str, repr,
    - grid_generation, integrate_pattern, add_enclosed_cells_to_pattern,
    - get_cell, get_movement, get_neighbor_coord, get_neighbors, find_dead_end,
    is_available, is_in_maze,
    - break_wall, add_wall, add_to_maze, path_to_not_in_maze,
    - check_consec_walls, dead_end_opener, room_closer, break_random_wall,
    - backtracking_algo, prim_algo, hunt_and_kill_algo,
    - choke_points_algo, braided_algo,
    - generate_maze, stepped_generation.

    #### Raises:
    - ValidationError
    - GenerationError

    Other possible Exceptions:
    - IndexError
    - AttributeError
    """
    generation_algorithms: tuple[str, ...] = (
        "Backtracking", "Prim", "Hunt_and_kill")

    imperfect_algorithms: tuple[str, str] = (
        "Choke_points", "Braided")

    def __init__(self, config: Config) -> None:
        """Initialises the attributes of the Maze instance."""

        self.width: MazeDimension = config.WIDTH
        self.height: MazeDimension = config.HEIGHT
        self.entry: CellCoordinates = config.ENTRY
        self.exit: CellCoordinates = config.EXIT
        self.perfect: bool = config.PERFECT
        self.gen_algorithm: str = config.GEN_ALGORITHM
        self.imperfect_algorithm: str = config.IMPERFECT_ALGORITHM
        self.seed: int = config.SEED
        set_seed(self.seed)

        self.pattern: list[list[bool]] = config.PATTERN
        self.pattern_h_offset: int = -1
        self.pattern_v_offset: int = -1
        if self.pattern != []:
            self.pattern_h_offset = (
                int(self.width / 2) - int(len(self.pattern[0]) / 2))
            self.pattern_v_offset = (
                int(self.height / 2) - int(len(self.pattern) / 2))

        self.cells: list[list[Maze.Cell]] = []
        self.initialized: bool = False
        self.generated: bool = False
        self.imperfected: bool = False
        self.pattern_implemented: bool = False

    def __str__(self) -> str:
        """Method to display a simplified view of the maze walls."""
        maze: str = "+---" * self.width + "+\n"
        for y in range(self.height):
            maze += "|" + "".join(
                "   |" if cell.walls[Directions.EAST] is True else "    "
                for cell in (
                    self.cells[x][y] for x in range(self.width))) + "\n"
            maze += "+" + "".join(
                "---+" if cell.walls[Directions.SOUTH] is True else "   +"
                for cell in (
                    self.cells[x][y] for x in range(self.width))) + "\n"
        return maze

    def __repr__(self) -> str:
        """Debug method displaying all information about the Maze."""
        return (
            f"{f"* Maze Attributes *":^40}\n"
            f"{"- Width:":<35}{self.width}\n"
            f"{"- Height:":<35}{self.height}\n"
            f"{"- Entry:":<35}{self.entry}\n"
            f"{"- Exit:":<35}{self.exit}\n"
            f"{"- Perfect:":<35}{self.perfect}\n"
            f"{"- Generation algorithm:":<35}{self.gen_algorithm}\n"
            f"{"- Imperfect algorithm:":<35}{self.imperfect_algorithm}\n"
            f"{"- Seed:":<35}{self.seed}\n\n"
            f"{f"* Pattern Attributes *":^40}\n"
            f"{"- Pattern width:":<35}{len(self.pattern[0])}\n"
            f"{"- Pattern height:":<35}{len(self.pattern)}\n"
            f"{"- Pattern horizontal offset:":<35}{self.pattern_h_offset}\n"
            f"{"- Pattern vertical offset:":<35}{self.pattern_v_offset}\n\n"
            f"{f"* Effective Maze Information *":^40}\n"
            f"{"- Cell matrix width:":<35}{len(self.cells)}\n"
            f"{"- Cell matrix height:":<35}{(
                len(self.cells[0]) if len(self.cells) > 0 else "-")}\n"
            f"{"- Initialized (existing grid):":<35}{self.initialized}\n"
            f"{"- Pattern implemented:":<35}{self.pattern_implemented}\n"
            f"{"- Generated (gen algorithm done):":<35}{self.generated}\n"
            f"{"- Imperfected (maze imperfected):":<35}{self.imperfected}\n"
        )

    class Cell:
        """Class Cell
        Atributes: coordinates, walls, entry, exit, pattern, is_in_maze,
        is_visited.
        Methods: init
        """
        def __init__(self, coordinates: CellCoordinates, walled: bool) -> None:
            """Initialises the attributes of the Cell instance."""
            self.coordinates: CellCoordinates = coordinates
            self.walls: list[bool] = [walled, walled, walled, walled]
            self.entry: bool = False
            self.exit: bool = False
            self.pattern: bool = False
            self.is_in_maze: bool = False
            self.is_visited: bool = False

    # _________________________________________________________________________
    #                         INITIALIZATION METHODS
    # _________________________________________________________________________

    def grid_generation(self, walled: bool) -> None:
        """Method to generate all the cells in the maze grid in a
        list[list[Maze.Cell]] Only the outer walls are set to True.
        Entry and Exit cells have their respective boolean set to True.
        """
        for x in range(self.width):
            self.cells.append([])
            for y in range(self.height):
                self.cells[x].append(Maze.Cell((x, y), walled))
        for cell in self.cells[0]:
            cell.walls[Directions.WEST] = True
        for cell in self.cells[-1]:
            cell.walls[Directions.EAST] = True
        for x in range(self.width):
            self.cells[x][0].walls[Directions.NORTH] = True
            self.cells[x][-1].walls[Directions.SOUTH] = True
        self.get_cell(self.entry).entry = True
        self.get_cell(self.exit).exit = True
        self.initialized = True
        self.integrate_pattern()

    def integrate_pattern(self) -> None:
        """Method that reads the given PATTERN and applies it to the current
        Maze, marking all concerned cells as pattern (attribute set to True),
        and marking up all their walls.
        """
        if self.pattern == []:
            return
        if self.initialized is False:
            raise GenerationError(
                self, "The maze was not initialized using the grid_generation "
                "or a global generation method before pattern implementation.")
        for x in range(len(self.pattern[0])):
            for y in range(len(self.pattern)):
                if self.pattern[y][x] is False:
                    continue
                self.cells[x + self.pattern_h_offset][
                    y + self.pattern_v_offset].pattern = True
                self.cells[x + self.pattern_h_offset][
                    y + self.pattern_v_offset].walls = [True, True, True, True]
        self.pattern_implemented = True

    def add_enclosed_cells_to_pattern(self) -> None:
        """Method to add every cells that weren't visited by the generating
        algorithm to the pattern, so they won't be selected during the
        making of an imperfect maze. This concerns cells enclosed by the
        pattern but not part of its drawing.
        """
        if self.pattern == []:
            return
        if self.initialized is False:
            raise GenerationError(
                self, "The maze was not initialized using the grid_generation "
                "or a global generation method before pattern implementation.")
        for x in range(self.pattern_h_offset,
                       self.pattern_h_offset + len(self.pattern[0])):
            for y in range(self.pattern_v_offset,
                           self.pattern_v_offset + len(self.pattern)):
                if self.cells[x][y].is_in_maze is True:
                    continue
                if (x, y) in (self.entry, self.exit):
                    raise GenerationError(
                        self, "The entry or exit point was placed in an "
                        "inaccessible cell (due to pattern).")
                self.cells[x][y].pattern = True

    # _________________________________________________________________________
    #                            MAZE INFO GETTERS
    # _________________________________________________________________________

    def get_cell(self, cell: CellCoordinates) -> Cell:
        """Returns the Cell object present at the given coordinates.
        Raises an IndexError if the cell is outside the maze.
        """
        return self.cells[cell[0]][cell[1]]

    def get_movement(
            self, source: CellCoordinates, dest: CellCoordinates) -> Movements:
        """Get the movement to apply when moving from the source cell to the
        destination. Because it fetches it from the Movements enum, if the
        given cells aren't neighbors, it will raise an AttributeError.
        """
        return Movements(((dest[0] - source[0]), (dest[1] - source[1])))

    def get_neighbor_coords(self, coords: CellCoordinates,
                            movement: tuple[int, int]) -> CellCoordinates:
        """Return the coordinates of the neighbor of the given cell(coords),
        in the specified direction.
        """
        neighbor: CellCoordinates = (
            coords[0] + movement[0], coords[1] + movement[1])
        return neighbor

    def get_neighbors(self, coords: CellCoordinates,
                      in_maze: bool | None = None) -> list[CellCoordinates]:
        """Return a list of available neighbors. The list can be filtered to
        include only neighbors that have been added to maze, those that aren't,
        or all of them without distinction.
        """
        neighbors: list[CellCoordinates] = []
        for movement in Movements:
            potential_neighbor = self.get_neighbor_coords(
                coords, movement.value)
            if self.is_available(potential_neighbor) is False:
                continue
            if (in_maze is not None and self.is_in_maze(potential_neighbor)
                    is not in_maze):
                continue
            neighbors.append(potential_neighbor)
        return neighbors

    def find_dead_end(self) -> list[CellCoordinates]:
        """Search all dead end in the maze, make a list of their coordinate
        and return it. Doesn't include dead-ends encased into the pattern.
        """
        dead_end: list[CellCoordinates] = []
        for y in range(0, (self.height)):
            for x in range(0, (self.width)):
                if (sum(not self.is_available(self.get_neighbor_coords((x, y),
                        move.value)) for move in Movements) < 3
                        and sum(self.cells[x][y].walls) == 3):
                    dead_end.append((x, y))
        shuffle(dead_end)
        return dead_end

    def is_available(self, coords: CellCoordinates) -> bool:
        """Check that a cell is accessible: within the grid and not reserved
        for the central pattern.
        """
        if (coords[0] < 0 or coords[1] < 0
                or coords[0] >= self.width
                or coords[1] >= self.height):
            return False
        if (self.pattern != [] and
                self.get_cell(coords).pattern is True):
            return False
        return True

    def is_in_maze(self, coords: CellCoordinates) -> bool:
        """Check whether a cell is part of the maze or not yet explored by
        the generation algorithm.
        """
        return self.get_cell(coords).is_in_maze

    # _________________________________________________________________________
    #                            GENERATION UTILS
    # _________________________________________________________________________

    def break_wall(self, coords: CellCoordinates,
                   neighbor: CellCoordinates) -> None:
        """Break down the wall between two cells. They must be directly
        adjacent to each other.
        """
        direction: Movements = self.get_movement(coords, neighbor)
        opposite: Movements = self.get_movement(neighbor, coords)
        self.get_cell(coords).walls[Directions[direction.name]] = False
        self.get_cell(neighbor).walls[Directions[opposite.name]] = False

    def add_wall(self, coords: CellCoordinates,
                 neighbor: CellCoordinates) -> None:
        """Add up a wall between two cells. They must be directly
        adjacent to each other.
        """
        direction: Movements = self.get_movement(coords, neighbor)
        opposite: Movements = self.get_movement(neighbor, coords)
        self.get_cell(coords).walls[Directions[direction.name]] = True
        self.get_cell(neighbor).walls[Directions[opposite.name]] = True

    def add_to_maze(self, coords: CellCoordinates) -> None:
        """Set the cell to is_in_maze = True."""
        self.get_cell(coords).is_in_maze = True

    def get_starting_point(self) -> CellCoordinates:
        """Return a random CellCoordinates for a cell situated in the maze,
        either anywhere if there is no pattern or between the maze edges and
        the pattern's offsets.
        """
        x_range: tuple[int, ...]
        y_range: tuple[int, ...]
        if self.pattern != []:
            x_range = tuple(
                x for x in range(0, (self.width - 1))
                if x not in range(
                    self.pattern_h_offset,
                    self.pattern_h_offset + len(self.pattern[0])))
            y_range = tuple(
                y for y in range(0, (self.height - 1))
                if y not in range(
                    self.pattern_v_offset,
                    self.pattern_v_offset + len(self.pattern)))
        else:
            x_range = tuple(x for x in range(0, self.width))
            y_range = tuple(y for y in range(0, self.height))
        start: CellCoordinates = (choice(x_range), choice(y_range))
        while self.is_available(start) is False:
            start = (choice(x_range), choice(y_range))
        return start

    def path_to_not_in_maze(self,
                            coords: CellCoordinates) -> CellCoordinates | None:
        """Find the neighbors that aren't yet in the maze of the cell with the
        coordinates passed as argument. Break down the walls between that cell
        and one of its randomly selected neighbors. Return the coordinate of
        the new cell in the maze, or None if the initial cell has no neighbors.
        """
        neighbors: list[CellCoordinates] = self.get_neighbors(coords, False)
        if neighbors == []:
            return None
        shuffle(neighbors)
        next_cell: CellCoordinates = neighbors[0]
        self.break_wall(coords, next_cell)
        self.add_to_maze(next_cell)
        return next_cell

    # _________________________________________________________________________
    #                       IMPERFECT MAZE GENERATION UTILS
    # _________________________________________________________________________

    def check_consec_walls(self) -> list[list[CellCoordinates]]:
        """Check if a wall is part of a sequence of 3+ consecutive walls
        along the horizontal or vertical axes of the grid. If it's the case
        it's added to the list of walls to be broken.
        Return the list of these walls."""
        walls_to_break: list[list[CellCoordinates]] = [[], []]
        consecutive_walls: int = 0
        for y in range(0, (self.height - 1)):
            for x in range(0, (self.width)):
                if self.cells[x][y].walls[Directions.SOUTH] is True:
                    consecutive_walls += 1
                    if consecutive_walls >= 3:
                        walls_to_break[0].append((x - 1, y))
                        consecutive_walls = 1
                else:
                    consecutive_walls = 0
            consecutive_walls = 0
        for x in range(0, (self.width - 1)):
            for y in range(0, (self.height)):
                if self.cells[x][y].walls[Directions.EAST] is True:
                    consecutive_walls += 1
                    if consecutive_walls >= 3:
                        walls_to_break[1].append((x, y - 1))
                        consecutive_walls = 1
                else:
                    consecutive_walls = 0
            consecutive_walls = 0
        return walls_to_break

    def dead_end_opener(self, anti_room: bool = True) -> Generator[None]:
        """Search dead end and make a path in an optimal way to avoid chambers
        in the maze. In order of priority: 1.Open the wall opposite the
        dead-end opening if the opposite cell is available. 2.Search for a
        dead-end with two True walls on the same side, perpendicular to the
        dead-end's entrance, to avoid creating chambers. 3.If no dead-end meets
        these criteria, then a random dead-end is chosen and one of the walls
        perpendicular to the entrance is opened if the adjacent cell is
        available.
        """
        dead_end: list[CellCoordinates] = self.find_dead_end()

        for coords in dead_end:
            entry_dir: int = self.get_cell(coords).walls.index(False)
            opposite_dir: int = ((entry_dir + 2) % 4)
            opposite_mov: tuple[int, int] = Movements[
                Directions(opposite_dir).name].value
            ideal_cell: CellCoordinates = self.get_neighbor_coords(
                coords, opposite_mov)
            if self.is_available(ideal_cell) is False:
                continue
            self.break_wall(coords, ideal_cell)
            yield None

        dead_end = self.find_dead_end()

        for coords in dead_end:
            entry_dir = self.get_cell(coords).walls.index(False)
            entry_mov: tuple[int, int] = Movements[
                Directions(entry_dir).name].value
            side_dir: tuple[int, int] = (
                ((entry_dir + 1) % 4), ((entry_dir + 3) % 4))
            cell_before_entry: CellCoordinates = self.get_neighbor_coords(
                coords, entry_mov)
            for side in side_dir:
                dead_end_walled: bool = self.get_cell(coords).walls[side]
                before_walled: bool = self.get_cell(
                    cell_before_entry).walls[side]
                if before_walled != dead_end_walled and anti_room is True:
                    continue
                side_mov: CellCoordinates = Movements[
                    Directions(side).name].value
                side_cell: CellCoordinates = self.get_neighbor_coords(
                    coords, side_mov)
                if self.is_available(side_cell) is True:
                    self.break_wall(coords, side_cell)
                    yield None
                    break

    def room_closer(self) -> Generator[None]:
        """Detect 'rooms', areas where four cells aren't separated by any wall,
        and add a new wall randomly to ensure every hallway in the maze is only
        1 cell large anywhere. Yields None every time a room is closed.
        """
        for x in range(0, self.width - 1):
            for y in range(0, self.height - 1):
                cell_group: tuple[CellCoordinates, ...] = (
                    (x, y), (x, y + 1), (x, y), (x + 1, y))
                if any(self.get_cell(cell).walls[Directions.EAST]
                        for cell in cell_group[:2]):
                    continue
                if any(self.get_cell(cell).walls[Directions.SOUTH]
                        for cell in cell_group[2:]):
                    continue
                rand_index: int = randint(0, 3)
                rand_cell: CellCoordinates = cell_group[rand_index]
                self.add_wall(rand_cell, self.get_neighbor_coords(
                    rand_cell, Movements.EAST.value
                    if rand_index in (0, 1) else Movements.SOUTH.value))
                yield None

    def break_random_wall(self) -> None:
        """Pick a dead-end from the dead-end list returned by the dedicated
        method, and break one of its side walls, because this method is only
        called after all dead-end have been remove by deleting their back
        wall. This is a fail-safe for the choke-points algorithm if the
        maze generation can't ensure the prevention of room creation within
        the maze.
        """
        for coords in self.find_dead_end():
            entry_dir = self.get_cell(coords).walls.index(False)
            side_dir: tuple[int, int] = (
                ((entry_dir + 1) % 4), ((entry_dir + 3) % 4))
            for side in side_dir:
                side_mov = Movements[Directions(side).name].value
                side_cell = ((coords[0] + side_mov[0]),
                             (coords[1] + side_mov[1]))
                if self.is_available(side_cell) is False:
                    continue
                self.break_wall(coords, side_cell)
                return

    # _________________________________________________________________________
    #                         GENERATION ALGORITHMS
    # _________________________________________________________________________

    def backtracking_algo(self) -> Generator[None]:
        """Generate a perfect maze with a backtraking algorithm.
        Return a Generator to display a dynamic maze.
        """
        if self.initialized is False:
            raise GenerationError(
                self, "Maze was not initialized using one of the implemented "
                "grid_generation, stepped_generation or generate_maze method.")

        start: CellCoordinates = self.get_starting_point()
        self.add_to_maze(start)

        back_track: list[CellCoordinates] = [start]
        while len(back_track) > 0:
            current: CellCoordinates = back_track[-1]
            next_cell = self.path_to_not_in_maze(current)
            if next_cell is not None:
                back_track.append(next_cell)
            else:
                back_track.pop(-1)
            yield None
        self.generated = True

    def prim_algo(self) -> Generator[None]:
        """Generate a perfect maze with a Prim algorithm.
        Return a Generator to display a dynamic maze.
        """
        if self.initialized is False:
            raise GenerationError(
                self, "Maze was not initialized using one of the implemented "
                "grid_generation, stepped_generation or generate_maze method.")

        starts: tuple[CellCoordinates, ...] = (
            (int((self.width - 1)/2), 0),
            (self.width - 1, int((self.height - 1)/2)),
            (int((self.width - 1)/2), self.height - 1),
            (0, int((self.height - 1)/2)))
        start: CellCoordinates = choice(starts)
        self.add_to_maze(start)

        frontiers: set[CellCoordinates] = set(self.get_neighbors(start, False))
        maze_cells: list[CellCoordinates] = [start, start]
        while frontiers:
            start = choice(list(frontiers))
            maze_cells.append(start)
            self.add_to_maze(start)
            frontiers.discard(start)
            for cell in reversed(maze_cells):
                direction: tuple[int, int] = (
                    cell[0] - start[0], cell[1] - start[1])
                if direction in Movements:
                    self.break_wall(start, cell)
                    break
            yield None
            frontiers.update(self.get_neighbors(start, False))
        self.generated = True

    def hunt_and_kill_algo(self) -> Generator[None]:
        """Generate a perfect maze with a Hunt and Kill algorithm.
        Return a Generator to display a dynamic maze.
        """
        if self.initialized is False:
            raise GenerationError(
                self, "Maze was not initialized using one of the implemented "
                "grid_generation, stepped_generation or generate_maze method.")

        start: CellCoordinates = self.get_starting_point()
        self.add_to_maze(start)

        def hunt_mode() -> CellCoordinates | None:
            """Function to hunt cell by cell from (0,0) to (width, height) and
            find the first cell who is not in maze and has at leat one neighbor
            which is in maze. Return that cell or None if no cell is found.
            """
            for y in range(0, (self.height)):
                for x in range(0, (self.width)):
                    current: CellCoordinates = (x, y)
                    neighbors: list[CellCoordinates] = self.get_neighbors(
                        current, True)
                    if (self.is_in_maze(current) is False
                            and neighbors != []
                            and self.is_available(current)):
                        cell_to_connect: CellCoordinates = choice(neighbors)
                        self.add_to_maze(current)
                        self.break_wall(current, cell_to_connect)
                        return current
                    continue
            return None

        while True:
            next_cell: CellCoordinates | None = self.path_to_not_in_maze(start)
            if next_cell is not None:
                self.add_to_maze(next_cell)
                self.break_wall(start, next_cell)
                start = next_cell
            else:
                new_start: CellCoordinates | None = hunt_mode()
                if new_start is None:
                    self.generated = True
                    return
                else:
                    start = new_start
            yield None

    # _________________________________________________________________________
    #                   IMPERFECT MAZE GENERATION ALGORITHMS
    # _________________________________________________________________________

    def choke_points_algo(self) -> Generator[None]:
        """Turn a perfect maze into an imperfect one by breaking walls that
        are 3 cells long, ensuring no room are created. If no wall can be
        broken that way, open up a single dead-end with dead-end opener.
        Yields None when walls a broken.
        """
        if self.generated is False:
            raise GenerationError(
                self, "Maze was not generated using an implemented algorithm "
                "before attempting to imperfect it")

        def break_east_wall(coords: CellCoordinates) -> None:
            """Break the wall between a cell and its right neighbor."""
            right_neighbor: CellCoordinates = (coords[0] + 1, coords[1])
            if (self.get_cell(coords).pattern is False
                    and self.get_cell(right_neighbor).pattern is False):
                self.get_cell(coords).walls[Directions.EAST] = False
                self.get_cell(right_neighbor).walls[Directions.WEST] = False
            else:
                v_walls.remove(coords)

        def break_south_wall(coords: CellCoordinates) -> None:
            """Break the wall between a cell and its down neighbor."""
            south_neighbor: CellCoordinates = (coords[0], coords[1] + 1)
            if (self.get_cell(coords).pattern is False
                    and self.get_cell(south_neighbor).pattern is False):
                self.get_cell(coords).walls[Directions.SOUTH] = False
                self.get_cell(south_neighbor).walls[Directions.NORTH] = False
            else:
                h_walls.remove(coords)

        h_walls: list[CellCoordinates]
        v_walls: list[CellCoordinates]
        h_walls, v_walls = self.check_consec_walls()
        for wall in v_walls:
            if randint(0, 100) < 85:
                break_east_wall(wall)
            yield None
        for wall in h_walls:
            if randint(0, 100) < 85:
                break_south_wall(wall)
            yield None
        if v_walls == [] and h_walls == []:
            for _ in self.dead_end_opener():
                break
            else:
                self.break_random_wall()
        self.imperfected = True

    def braided_algo(self) -> Generator[None]:
        """Imperfect algorithm which purpose is to open up loops within the
        maze by eliminating every dead-end. Loops through 3 actions until the
        only remaining dead-ends are caused by the pattern, ensuring no room
        is created in the process.
        - Open up dead-ends first through their back wall, then their side
        wall if their back wall leads outside the maze, sometimes creating
        rooms.
        - Open up the angles of the maze by moving the sidewall that's inside
        the maze inward, sometimes creating other dead-end.
        - Close down rooms by placing randomly a wall inside each of them,
        sometimes creating dead-ends.
        Loops and yields None for each action until no dead-end are to be
        found. Edge cases may generate infinite loops.
        """
        if self.generated is False:
            raise GenerationError(
                self, "Maze was not generated using an implemented algorithm "
                "before attempting to imperfect it")
        while len(self.find_dead_end()) != 0:
            for _ in self.dead_end_opener(False):
                yield None
            for _ in self.room_closer():
                yield None
        self.imperfected = True

    # _________________________________________________________________________
    #                       MAZE GENERATION TRIGGERS
    # _________________________________________________________________________

    def generate_maze(self) -> None:
        """Generate the maze with the algorithm given in config, and make it
        imperfect if perfect is set to False. The generation is done and the
        maze is display after it.
        """
        self.grid_generation(True)
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Backtracking": self.backtracking_algo,
            "Prim": self.prim_algo,
            "Hunt_and_kill": self.hunt_and_kill_algo,
            "Choke_points": self.choke_points_algo,
            "Braided": self.braided_algo}
        for _ in algorithms[self.gen_algorithm]():
            pass
        self.add_enclosed_cells_to_pattern()
        if self.perfect is False:
            for _ in algorithms[self.imperfect_algorithm]():
                pass

    def stepped_generation(self) -> Generator[None]:
        """Generate the maze with the algorithm given in config, and make it
        imperfect if perfect is set to False. The display is done during the
        generation, making it dynamic.
        """
        self.grid_generation(True)
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Backtracking": self.backtracking_algo,
            "Prim": self.prim_algo,
            "Hunt_and_kill": self.hunt_and_kill_algo,
            "Choke_points": self.choke_points_algo,
            "Braided": self.braided_algo}
        for _ in algorithms[self.gen_algorithm]():
            yield None
        self.add_enclosed_cells_to_pattern()
        if self.perfect is False:
            for _ in algorithms[self.imperfect_algorithm]():
                yield None


if __name__ == "__main__":
    """Entry point of the program"""
    from time import sleep
    config: Config = Config(
        WIDTH=10,
        HEIGHT=10,
        ENTRY=(0, 0),
        EXIT=(0, 1),
        PERFECT=False,
        GEN_ALGORITHM="Prim",
        IMPERFECT_ALGORITHM="Braided",
        SEED=randint(0, 99999999),
        PATTERN=[
            [False, False, True, False, True, True, True],
            [False, True, False, False, False, False, True],
            [True, True, True, False, False, True, False],
            [False, False, True, False, True, False, False],
            [False, False, True, False, True, True, True]])
    maze: Maze = Maze(config)
    print(maze.__repr__())
    for _ in maze.stepped_generation():
        print("\033[3J\033[1;0H\033[0J")
        print(maze)
        sleep(0.01)
    print(maze.__repr__())
