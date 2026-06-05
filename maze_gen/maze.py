
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
    WEST = (-1, 0)
    SOUTH = (0, +1)
    EAST = (+1, 0)
    NORTH = (0, -1)


class Maze:
    """Class Maze.
    Attributes: width, height, entry, exit, perfect, seed,
    central_icon, config, cells.
    Methods: generation(), repr().
    Nested_class: Config, Cell.
    """
    def __init__(
            self, width: int, height: int,
            entry: tuple[int, int], exit: tuple[int, int],
            perfect: bool, gen_algorithm: str,
            seed: int, central_icon: bool = False):
        self.config = Maze.Config(
            WIDTH=width,
            HEIGHT=height,
            ENTRY=entry,
            EXIT=exit,
            PERFECT=perfect,
            GEN_ALGORITHM=gen_algorithm,
            SEED=seed,
            CENTRAL_ICON=central_icon)
        set_seed(self.config.SEED)
        self.cells: list[list[Maze.Cell]] = []

    class Config(BaseModel):
        """Class Config
        Attributes: WIDTH, HEIGHT, ENTRY, EXIT, CENTRAL_ICON, PERFECT, SEED.
        Methods: validate_config(), str().
        """
        WIDTH: MazeDimension
        HEIGHT: MazeDimension
        ENTRY: CellCoordinates
        EXIT: CellCoordinates

        GEN_ALGORITHM: Annotated[str, Field(min_length=1, max_length=15)]

        CENTRAL_ICON: Annotated[bool, Field(default=False)]
        PERFECT: Annotated[bool, Field()]
        SEED: Annotated[int, Field()]

        @model_validator(mode='after')
        def validate_config(self) -> "Maze.Config":
            """Model validator for maze's configuration."""
            error_message: str = ""
            if self.CENTRAL_ICON is True and (
                    self.WIDTH < 7 or self.HEIGHT < 7):
                error_message += (
                    "Generating a maze with dimensions inferior to 7 by 7 is "
                    "impossible when integrating the central pattern.")
            if self.ENTRY[0] >= self.WIDTH or self.ENTRY[1] >= self.HEIGHT:
                error_message += (
                    "Entry coordinates (x, y) "
                    "cannot exceed the maze's dimensions")
            if self.EXIT[0] >= self.WIDTH or self.EXIT[1] >= self.HEIGHT:
                error_message += (
                    "Exit coordinates (x, y) "
                    "cannot exceed the maze's dimensions")
            if error_message != "":
                raise ValueError(error_message)
            return self

        def __str__(self) -> str:
            """Method to display configuration of the maze (width, height,
            entry, exit, icon toggle, perfect toggle and seed).
            """
            return (
                f"WIDTH: {self.WIDTH}, HEIGHT: {self.HEIGHT}\n"
                f"ENTRY: {self.ENTRY}, EXIT: {self.EXIT}\n"
                f"ICON TOGGLE: {self.CENTRAL_ICON}, "
                f"PERFECT TOGGLE: {self.PERFECT}\nSEED: {self.SEED}")

    class Cell:
        """Class Cell
        Atributes: coordinates: bool, walls: list[bool], entry: bool,
        exit: bool, pattern: bool.
        """
        def __init__(self, coordinates: CellCoordinates, walled: bool):
            self.coordinates: CellCoordinates = coordinates
            self.walls: list[bool] = [walled, walled, walled, walled]
            self.entry = False
            self.exit = False
            self.pattern = False
            self.is_visited = False

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

    # _________________________________________________________________________
    #                       GENERATION/SOLVING TOOLS
    # _________________________________________________________________________

    def get_neighbor_coords(self, coords: CellCoordinates,
                            movement: tuple[int, int]) -> CellCoordinates:
        """Return the coordinates of the neighboring cell in the specified
        direction.
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
                self.config.CENTRAL_ICON is True and
                self.cells[coords[0]][
                coords[1]].pattern is True):
            return False
        return True

    def is_visited(self, coords: CellCoordinates) -> bool:
        """Check whether a cell is visited or not."""
        return self.cells[coords[0]][coords[1]].is_visited

    def get_neighbors(self, coords: CellCoordinates,
                      visited: bool | None) -> list[CellCoordinates]:
        """Return a list of available neighbors. The list can be filtered to
        include only neighbors that have been visited, those that aren't, or
        all of them without distinction.
        """
        neighbors: list[CellCoordinates] = []
        for movement in Movements:
            potential_neighbor = self.get_neighbor_coords(
                coords, movement.value)
            if self.is_available(potential_neighbor) is False:
                continue
            if (visited is not None and self.is_visited(potential_neighbor)
                    is not visited):
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

    def become_visited(self, coords: CellCoordinates) -> None:
        """Set the cell to is_visited = True."""
        self.cells[coords[0]][coords[1]].is_visited = True

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
        self.become_visited(next_cell)
        return next_cell

    def check_consec_walls(self, axes: str) -> list[CellCoordinates]:
        """Check if a wall is part of a sequence of 3+ consecutive walls
        along the horizontal or vertical axes of the grid. If it's the case
        it has 80% chance to be added to the lis of walls to be broken.
        Return the list of these walls."""
        walls_to_broke: list[CellCoordinates] = []
        consecutive_walls: int = 0
        if axes == "horizontal":
            for y in range(0, (self.config.HEIGHT - 1)):
                for x in range(0, (self.config.WIDTH)):
                    if self.cells[x][y].walls[1] is True:
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
                    if self.cells[x][y].walls[2] is True:
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
        in the maze."""
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
        self.become_visited(start)

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
        self.become_visited(start)
        frontiers: set[CellCoordinates] = set(self.get_neighbors(start, False))
        maze_cells: list[CellCoordinates] = [start, start]
        while frontiers:
            start = choice(list(frontiers))
            maze_cells.append(start)
            self.become_visited(start)
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
        self.become_visited(start)

        def hunt_mode() -> CellCoordinates | None:
            """Function to hunt cell by cell from (0,0) to (width, height) and
            find the first cell who is unvisited and has at leat one neighbor
            which is visited. Return that cell or None if no cell is found."""
            for y in range(0, (self.config.HEIGHT)):
                for x in range(0, (self.config.WIDTH)):
                    current: CellCoordinates = (x, y)
                    neighbors: list[CellCoordinates] = self.get_neighbors(
                        current, True)
                    if self.is_visited(current) is False and neighbors != []:
                        print(neighbors)
                        cell_to_connect: CellCoordinates = choice(neighbors)
                        self.become_visited(current)
                        self.break_wall(current, cell_to_connect)
                        return current
                    continue
            return None

        new_start: CellCoordinates | None
        while True:
            next_cell = self.path_to_unvisited(start)
            if next_cell is not None:
                self.become_visited(next_cell)
                self.break_wall(start, next_cell)
                start = next_cell
            else:
                new_start = hunt_mode()
                if new_start is None:
                    return
                else:
                    start = new_start
            yield None

    def make_maze_imperfect(self) -> None:
        """Make an imperfect maze from a perfect one. Use check_consec_walls()
        method to have all the walls to broke. If there is none, use
        dead_end_opener() method.
        """
        def break_east_wall(coords: CellCoordinates) -> None:
            """Break the wall between a cell and her right neighbor."""
            self.cells[coords[0]][coords[1]].walls[Directions.EAST] = False
            self.cells[coords[0] + 1][coords[1]].walls[Directions.WEST] = False

        def break_south_wall(coords: CellCoordinates) -> None:
            """Break the wall between a cell and her down neighbor."""
            self.cells[coords[0]][coords[1]].walls[
                Directions.SOUTH] = False
            self.cells[coords[0]][coords[1] + 1].walls[
                Directions.NORTH] = False

        v_walls: list[CellCoordinates] = self.check_consec_walls("vertical")
        h_walls: list[CellCoordinates] = self.check_consec_walls("horizontal")
        for wall in v_walls:
            break_east_wall(wall)
        for wall in h_walls:
            break_south_wall(wall)
        if v_walls == [] and h_walls == []:
            self.dead_end_opener()

    # _________________________________________________________________________
    #                            SOLVING ALGORITHMS
    # _________________________________________________________________________

    def breadth_first_search_algorithm(self) -> None:
        """"""

    def dead_end_filling_algorithm(self) -> None:
        """"""

    def dijkstra_algorithm(self) -> None:
        """"""

    def alpha_star_algorithm(self) -> None:
        """"""

    # _________________________________________________________________________
    #                         MAZE GENERATION AND DISPLAY
    # _________________________________________________________________________

    def generate_maze(self) -> None:
        self.grid_generation(True)
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Backtracking": self.backtracking_algo,
            "Prim": self.prim_algo,
            "Hunt_and_kill": self.hunt_and_kill_algo}
        for _ in algorithms[self.config.GEN_ALGORITHM]():
            pass
        if self.config.PERFECT is False:
            self.make_maze_imperfect()

    def stepped_generation(self) -> Generator[None]:
        self.grid_generation(True)
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Backtracking": self.backtracking_algo,
            "Prim": self.prim_algo,
            "Hunt_and_kill": self.hunt_and_kill_algo}
        for _ in algorithms[self.config.GEN_ALGORITHM]():
            yield None
        if self.config.PERFECT is False:
            self.make_maze_imperfect()

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
        gen_algorithm="Hunt_and_kill",
        seed=randint(0, 99999999),
        central_icon=False
    )
    print(maze.config)
    for _ in maze.stepped_generation():
        print("\033[3J\033[1;0H\033[0J")
        print(maze)
        sleep(0.01)
    print(maze)
