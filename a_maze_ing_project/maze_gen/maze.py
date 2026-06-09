
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
    Enum for west(-1, 0), south(0, +1), east(+1, 0)
    and north(0, -1). Each direction is associated with
    a tuple of x, y movements to go on the given direction.
    """
    WEST = (-1, 0)
    SOUTH = (0, +1)
    EAST = (+1, 0)
    NORTH = (0, -1)


class Maze:
    """Class Maze.
    Nested_class: Config, Cell.
    Attributes: width, height, entry, exit, perfect,
    gen_algorithm, seed, pattern, config, cells.
    Methods: init, integrate_pattern, add_enclosed_cells_to_pattern,
    grid_generation,get_neighbor_coord, is_available, is_in_maze,
    get_neighbors, break_wall, add_to_maze, path_to_unvisited,
    check_consec_walls, find_dead_end, dead_end_opener, backtracking_algo,
    prim_algo, hunt_and_kill_algo, make_maze_imperfect, generate_maze,
    stepped_generation, repr.
    """
    generation_algorithms: tuple[str, ...] = (
        "Backtracking", "Prim", "Hunt_and_kill")

    def __init__(
        """Initialises the attributes of the Maze instance."""
            self, width: int, height: int,
            entry: tuple[int, int], exit: tuple[int, int],
            perfect: bool, gen_algorithm: str, seed: int,
            pattern: list[list[bool]] = []):
        if gen_algorithm not in self.generation_algorithms:
            raise ValueError(
                f"Invalid generation algorithm entered: {gen_algorithm}. "
                f"Available: {", ".join(self.generation_algorithms)}")
        self.config = Maze.Config(
            WIDTH=width,
            HEIGHT=height,
            ENTRY=entry,
            EXIT=exit,
            PERFECT=perfect,
            GEN_ALGORITHM=gen_algorithm,
            SEED=seed,
            PATTERN=pattern)
        set_seed(self.config.SEED)
        self.cells: list[list[Maze.Cell]] = []
        if self.config.PATTERN != []:
            self.pattern_h_offset: int = (
                int(self.config.WIDTH / 2)
                - int(len(self.config.PATTERN[0]) / 2))
            self.pattern_v_offset: int = (
                int(self.config.HEIGHT / 2)
                - int(len(self.config.PATTERN) / 2))

    class Config(BaseModel):
        """Class Config
        Attributes: WIDTH, HEIGHT, ENTRY, EXIT, GEN_ALGORITHM,
        PATTERN, PERFECT, SEED.
        Methods: validate_config.
        """
        WIDTH: MazeDimension
        HEIGHT: MazeDimension
        ENTRY: CellCoordinates
        EXIT: CellCoordinates

        GEN_ALGORITHM: Annotated[str, Field(min_length=1, max_length=15)]

        PATTERN: Annotated[list[list[bool]], Field(default=[])]
        PERFECT: Annotated[bool, Field()]
        SEED: Annotated[int, Field()]

        @model_validator(mode='after')
        def validate_config(self) -> "Maze.Config":
            """Model validator for maze's configuration."""
            error_message: str = ""
            if self.PATTERN != []:
                if all(
                        len(line) == len(self.PATTERN[0])
                        for line in self.PATTERN) is False:
                    error_message += (
                        "The integrated pattern must be a tuple of tuple "
                        "containing boolean values only, with each line "
                        "being the same length.")
                if (
                        self.WIDTH < len(self.PATTERN[0]) + 2
                        or self.HEIGHT < len(self.PATTERN) + 2):
                    error_message += (
                        "Generating a maze when integrating the central "
                        "pattern must be done with appropriate dimensions.")
                for x in range(len(self.PATTERN[0])):
                    for y in range(len(self.PATTERN)):
                        if self.PATTERN[y][x] is True:
                            pattern_h_offset: int = (
                                int(self.WIDTH / 2)
                                - int(len(self.PATTERN[0]) / 2))
                            pattern_v_offset: int = (
                                int(self.HEIGHT / 2)
                                - int(len(self.PATTERN) / 2))
                            in_pattern_coords: CellCoordinates = (
                                x + pattern_h_offset,
                                y + pattern_v_offset)
                            if (
                                    in_pattern_coords == self.ENTRY
                                    or in_pattern_coords == self.EXIT):
                                error_message += (
                                    "Entry and Exit coordinates cannot be "
                                    "placed in pattern cells.")
            if self.ENTRY[0] >= self.WIDTH or self.ENTRY[1] >= self.HEIGHT:
                error_message += (
                    "Entry coordinates (x, y) "
                    "cannot exceed the maze's dimensions.")
            if self.EXIT[0] >= self.WIDTH or self.EXIT[1] >= self.HEIGHT:
                error_message += (
                    "Exit coordinates (x, y) "
                    "cannot exceed the maze's dimensions.")
            if error_message != "":
                raise ValueError(error_message)
            return self

    class Cell:
        """Class Cell
        Atributes: coordinates, walls, entry, exit, pattern, is_in_maze,
        is_visited.
        Methods: init
        """
        def __init__(self, coordinates: CellCoordinates, walled: bool):
            self.coordinates: CellCoordinates = coordinates
            self.walls: list[bool] = [walled, walled, walled, walled]
            self.entry: bool = False
            self.exit: bool = False
            self.pattern: bool = False
            self.is_in_maze: bool = False
            self.is_visited: bool = False

    def integrate_pattern(self) -> None:
        """Method that reads the given PATTERN and applies it to the current
        Maze, marking all concerned cells as pattern (attribute set to True),
        and marking up all their walls.
        """
        for x in range(len(self.config.PATTERN[0])):
            for y in range(len(self.config.PATTERN)):
                if self.config.PATTERN[y][x] is False:
                    continue
                self.cells[x + self.pattern_h_offset][
                    y + self.pattern_v_offset].pattern = True
                self.cells[x + self.pattern_h_offset][
                    y + self.pattern_v_offset].walls = [True, True, True, True]

    def add_enclosed_cells_to_pattern(self) -> None:
        """Method to add every cells that weren't visited by the generating
        algorithm to the pattern, so they won't be selected during the
        making of an imperfect maze. This concerns cells enclosed by the
        pattern but not part of its drawing.
        """
        for x in range(len(self.config.PATTERN[0])):
            for y in range(len(self.config.PATTERN)):
                if self.cells[x + self.pattern_h_offset][
                        y + self.pattern_v_offset].is_in_maze is False:
                    self.cells[x + self.pattern_h_offset][
                        y + self.pattern_v_offset].pattern = True

    def grid_generation(self, walled: bool) -> None:
        """Method to generate all the cells in the maze grid in a
        list[list[Maze.Cell]] Only the outer walls are set to True.
        Entry and Exit cells are memorized.
        """
        for x in range(self.config.WIDTH):
            self.cells.append([])
            for y in range(self.config.HEIGHT):
                self.cells[x].append(Maze.Cell((x, y), walled))
        for cell in self.cells[0]:
            cell.walls[Directions.WEST] = True
        for cell in self.cells[-1]:
            cell.walls[Directions.EAST] = True
        for x in range(self.config.WIDTH):
            self.cells[x][0].walls[Directions.NORTH] = True
            self.cells[x][-1].walls[Directions.SOUTH] = True
        self.cells[self.config.ENTRY[0]][self.config.ENTRY[1]].entry = True
        self.cells[self.config.EXIT[0]][self.config.EXIT[1]].exit = True
        if self.config.PATTERN != []:
            self.integrate_pattern()

    # _________________________________________________________________________
    #                            GENERATION UTILS
    # _________________________________________________________________________

    def get_neighbor_coords(self, coords: CellCoordinates,
                            movement: tuple[int, int]) -> CellCoordinates:
        """Return the coordinates of the neighbor of the given cell(coords),
        in the specified direction.
        """
        neighbor: CellCoordinates = (coords[0] + movement[0],
                                     coords[1] + movement[1])
        return neighbor

    def is_available(self, coords: CellCoordinates) -> bool:
        """Check that a cell is accessible: within the grid and not reserved
        for the central pattern.
        """
        if (
                coords[0] < 0 or coords[1] < 0
                or coords[0] >= self.config.WIDTH
                or coords[1] >= self.config.HEIGHT):
            return False
        if (
                self.config.PATTERN != [] and
                self.cells[coords[0]][
                coords[1]].pattern is True):
            return False
        return True

    def is_in_maze(self, coords: CellCoordinates) -> bool:
        """Check whether a cell is in the maze or not."""
        return self.cells[coords[0]][coords[1]].is_in_maze

    def get_neighbors(self, coords: CellCoordinates,
                      in_maze: bool | None) -> list[CellCoordinates]:
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

    def break_wall(self, coords: CellCoordinates,
                   neighbor: CellCoordinates) -> None:
        """Break down the wall between two cells. They must be directly
        adjacent to each other.
        """
        direction = Movements(((neighbor[0] - coords[0]),
                               (neighbor[1] - coords[1])))
        opposite = Movements((-(neighbor[0] - coords[0]),
                              -(neighbor[1] - coords[1])))
        self.cells[coords[0]][coords[1]].walls[
            Directions[direction.name]] = False
        self.cells[neighbor[0]][neighbor[1]].walls[
            Directions[opposite.name]] = False

    def add_to_maze(self, coords: CellCoordinates) -> None:
        """Set the cell to is_in_maze = True."""
        self.cells[coords[0]][coords[1]].is_in_maze = True

    def path_to_unvisited(self,
                          coords: CellCoordinates) -> CellCoordinates | None:
        """Find the neighbors of the cell with the coordinates passed as an
        argument. Break down the walls between that cell and one of its
        randomly selected neighbors. Return the coordinate of the new cell in
        the maze, or None if the initial cell has no neighbors.
        """
        neighbors: list[CellCoordinates] = self.get_neighbors(coords, False)
        if neighbors == []:
            return None
        shuffle(neighbors)
        next_cell = neighbors[0]
        self.break_wall(coords, next_cell)
        self.add_to_maze(next_cell)
        return next_cell

    def check_consec_walls(self, axes: str) -> list[CellCoordinates]:
        """Check if a wall is part of a sequence of 3+ consecutive walls
        along the horizontal or vertical axes of the grid. If it's the case
        it has 80% chance to be added to the list of walls to be broken.
        Return the list of these walls."""
        walls_to_broke: list[CellCoordinates] = []
        consecutive_walls: int = 0
        if axes == "horizontal":
            for y in range(0, (self.config.HEIGHT - 1)):
                for x in range(0, (self.config.WIDTH)):
                    if self.cells[x][y].walls[Directions.SOUTH] is True:
                        consecutive_walls += 1
                        if consecutive_walls >= 3 and randint(0, 100) < 80:
                            walls_to_broke.append((x - 1, y))
                            consecutive_walls = 1
                    else:
                        consecutive_walls = 0
                consecutive_walls = 0
        if axes == "vertical":
            for x in range(0, (self.config.WIDTH - 1)):
                for y in range(0, (self.config.HEIGHT)):
                    if self.cells[x][y].walls[Directions.EAST] is True:
                        consecutive_walls += 1
                        if consecutive_walls >= 3 and randint(0, 100) < 80:
                            walls_to_broke.append((x, y - 1))
                            consecutive_walls = 1
                    else:
                        consecutive_walls = 0
                consecutive_walls = 0
        return walls_to_broke

    def find_dead_end(self) -> list[CellCoordinates]:
        """Search all dead end in the maze, make a list of their coordinate
        and return it.
        """
        dead_end: list[CellCoordinates] = []
        for y in range(0, (self.config.HEIGHT)):
            for x in range(0, (self.config.WIDTH)):
                if sum(self.cells[x][y].walls) == 3:
                    dead_end.append((x, y))
        shuffle(dead_end)
        return dead_end

    def dead_end_opener(self) -> None:
        """Search dead end and make a path in an optimal way to avoid chambers
        in the maze. In order of priority: 1.Open the wall opposite the
        dead-end opening if the opposite cell is available. 2.Search for a
        dead-end with two True walls on the same side, perpendicular to the
        dead-end’s entrance, to avoid creating chambers. 3.If no dead-end meets
        these criteria, then a random dead-end is chosen and one of the walls
        perpendicular to the entrance is opened if the adjacent cell is available.
        """
        dead_end: list[CellCoordinates] = self.find_dead_end()

        for coord in dead_end:
            entry_dir: int = self.cells[
                coord[0]][coord[1]].walls.index(False)
            opposite_dir: int = ((entry_dir + 2) % 4)
            opposite_mov: tuple[int, int] = Movements(
                Directions(opposite_dir).name).value
            ideal_cell: CellCoordinates = ((coord[0] + opposite_mov[0]),
                                           (coord[1] + opposite_mov[1]))
            if self.is_available(ideal_cell) is False:
                continue
            self.break_wall(coord, ideal_cell)
            return

        for coord in dead_end:
            entry_dir = self.cells[
                coord[0]][coord[1]].walls.index(False)
            entry_mov: tuple[int, int] = Movements(
                Directions(entry_dir).name).value
            cell_before_entry: CellCoordinates = (
                    (coord[0] + entry_mov[0]),
                    (coord[1] + entry_mov[1]))
            side_dir: list[int] = [((entry_dir + 1) % 4),
                                   ((entry_dir + 3) % 4)]
            for side in side_dir:
                dead_end_walled: bool = self.cells[
                    coord[0]][coord[1]].walls[side]
                before_walled: bool = self.cells[
                    cell_before_entry[0]][cell_before_entry[1]].walls[side]
                if before_walled != dead_end_walled:
                    continue
                side_mov: CellCoordinates = Movements[
                    Directions(side).name].value
                side_cell: CellCoordinates = ((coord[0] + side_mov[0]),
                                              (coord[1] + side_mov[1]))
                if self.is_available(side_cell) is True:
                    self.break_wall(coord, side_cell)
                    return

        for coord in dead_end:
            entry_dir = self.cells[
                coord[0]][coord[1]].walls.index(False)
            side_dir = [((entry_dir + 1) % 4),
                        ((entry_dir + 3) % 4)]
        for side in side_dir:
            side_mov = Movements[
                Directions(side).name].value
            side_cell = (
                (coord[0] + side_mov[0]),
                (coord[1] + side_mov[1]))
            if self.is_available(side_cell) is False:
                continue
            self.break_wall(coord, side_cell)
            return

    # _________________________________________________________________________
    #                         GENERATION ALGORITHMS
    # _________________________________________________________________________

    def backtracking_algo(self) -> Generator[None]:
        """Generate a perfect maze with a backtraking algorithm.
        Return a Generator to display a dynamic maze.
        """
        start: CellCoordinates = (randint(0, (self.config.WIDTH - 1)),
                                  randint(0, (self.config.HEIGHT - 1)))
        while self.is_available(start) is False:
            start = (randint(0, (self.config.WIDTH - 1)),
                     randint(0, (self.config.HEIGHT - 1)))
        self.add_to_maze(start)

        back_track: list[CellCoordinates] = [start]
        while back_track:
            current: CellCoordinates = back_track[-1]
            next_cell = self.path_to_unvisited(current)
            if next_cell is not None:
                back_track.append(next_cell)
            else:
                back_track.pop(-1)
            yield None

    def prim_algo(self) -> Generator[None]:
        """Generate a perfect maze with a Prim algorithm.
        Return a Generator to display a dynamic maze.
        """
        starts: tuple[CellCoordinates, ...] = (
            (int((self.config.WIDTH - 1)/2), 0),
            (self.config.WIDTH - 1, int((self.config.HEIGHT - 1)/2)),
            (int((self.config.WIDTH - 1)/2), self.config.HEIGHT - 1),
            (0, int((self.config.HEIGHT - 1)/2)))
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

    def hunt_and_kill_algo(self) -> Generator[None]:
        """Generate a perfect maze with a Hunt and Kill algorithm.
        Return a Generator to display a dynamic maze.
        """
        starts: tuple[CellCoordinates, ...] = (
            (self.config.WIDTH - 1, int((self.config.HEIGHT - 1)/2)),
            (int((self.config.WIDTH - 1)/2), self.config.HEIGHT - 1),
            (0, int((self.config.HEIGHT - 1)/2)))
        start: CellCoordinates = choice(starts)
        self.add_to_maze(start)

        def hunt_mode() -> CellCoordinates | None:
            """Function to hunt cell by cell from (0,0) to (width, height) and
            find the first cell who is not in maze and has at leat one neighbor
            which is in maze. Return that cell or None if no cell is found.
            """
            for y in range(0, (self.config.HEIGHT)):
                for x in range(0, (self.config.WIDTH)):
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

        new_start: CellCoordinates | None
        while True:
            next_cell = self.path_to_unvisited(start)
            if next_cell is not None:
                self.add_to_maze(next_cell)
                self.break_wall(start, next_cell)
                start = next_cell
            else:
                new_start = hunt_mode()
                if new_start is None:
                    return
                else:
                    start = new_start
            yield None

    def make_maze_imperfect(self) -> Generator[None]:
        """Make an imperfect maze from a perfect one. Use check_consec_walls()
        method to have all the walls to broke. If there is none, use
        dead_end_opener() method.
        """
        def break_east_wall(coords: CellCoordinates) -> None:
            """Break the wall between a cell and her right neighbor."""
            if (self.cells[coords[0]][coords[1]].pattern is False
                    and self.cells[coords[0] + 1][coords[1]].pattern is False):
                self.cells[coords[0]][coords[1]].walls[
                    Directions.EAST] = False
                self.cells[coords[0] + 1][coords[1]].walls[
                    Directions.WEST] = False
            else:
                v_walls.remove(coords)

        def break_south_wall(coords: CellCoordinates) -> None:
            """Break the wall between a cell and her down neighbor."""
            if (self.cells[coords[0]][coords[1]].pattern is False
                    and self.cells[coords[0]][coords[1] + 1].pattern is False):
                self.cells[coords[0]][coords[1]].walls[
                    Directions.SOUTH] = False
                self.cells[coords[0]][coords[1] + 1].walls[
                    Directions.NORTH] = False
            else:
                h_walls.remove(coords)

        v_walls: list[CellCoordinates] = self.check_consec_walls("vertical")
        h_walls: list[CellCoordinates] = self.check_consec_walls("horizontal")
        for wall in v_walls:
            break_east_wall(wall)
            yield None
        for wall in h_walls:
            break_south_wall(wall)
            yield None
        if v_walls == [] and h_walls == []:
            self.dead_end_opener()

    # _________________________________________________________________________
    #                         MAZE GENERATION AND DISPLAY
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
            "Hunt_and_kill": self.hunt_and_kill_algo}
        for _ in algorithms[self.config.GEN_ALGORITHM]():
            pass
        self.add_enclosed_cells_to_pattern()
        if self.config.PERFECT is False:
            for _ in self.make_maze_imperfect():
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
            "Hunt_and_kill": self.hunt_and_kill_algo}
        for _ in algorithms[self.config.GEN_ALGORITHM]():
            yield None
        self.add_enclosed_cells_to_pattern()
        if self.config.PERFECT is False:
            for _ in self.make_maze_imperfect():
                yield None

    def __repr__(self) -> str:
        """Method to display debug mode of the maze walls."""
        maze: str = "+---" * self.config.WIDTH + "+\n"
        for y in range(self.config.HEIGHT):
            maze += "|" + "".join(
                "   |" if cell.walls[Directions.EAST] is True else "    "
                for cell in (self.cells[x][y]
                             for x in range(self.config.WIDTH))) + "\n"
            maze += "+" + "".join(
                "---+" if cell.walls[Directions.SOUTH] is True else "   +"
                for cell in (self.cells[x][y]
                             for x in range(self.config.WIDTH))) + "\n"
        return maze


if __name__ == "__main__":
    """Entry point of the program"""
    from time import sleep
    maze = Maze(
        width=25,
        height=25,
        entry=(0, 0),
        exit=(0, 1),
        perfect=False,
        gen_algorithm="Prim",
        seed=randint(0, 99999999),
        pattern=[
            [False, False, True, False, True, True, True],
            [False, True, False, False, False, False, True],
            [True, True, True, False, False, True, False],
            [False, False, True, False, True, False, False],
            [False, False, True, False, True, True, True]]
    )
    print(maze.config)
    for _ in maze.stepped_generation():
        print("\033[3J\033[1;0H\033[0J")
        print(maze)
        sleep(0.01)
    print(maze)
