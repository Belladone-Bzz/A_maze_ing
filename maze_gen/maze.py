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

    def generation(self, walled: bool) -> None:
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

    def open_wall(self, cell_coords: CellCoordinates, step: Movements) -> None:
        self.cells[cell_coords[0]][cell_coords[1]].walls[step] = False
        self.cells[cell_coords[0] + step[0]][cell_coords[1] + step[1]].walls[
            Directions[Movements((-step[0], -step[1])).name]] = False

    # _________________________________________________________________________
    #                                   TOOLS
    # _________________________________________________________________________

    def get_neighbor_coords(self, coords: CellCoordinates, movement: tuple[int, int]) -> CellCoordinates:
        """Return the coordinates of the neighboring cell in the specified direction."""
        neighbor: CellCoordinates = (coords[0] + movement[0], coords[1] + movement[1])
        return neighbor
    
    def is_available(self, coords: CellCoordinates) -> bool:
        "Check that a cell is accessible: within the grid and not reserved for the central pattern."
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
    
    def get_neighbors(self, coords: CellCoordinates, visited: bool | None) -> list[CellCoordinates]:
        """Return a list of available neighbors. The list can be filtered to include only neighbors that have been visited, those that aren't, or all of them without distinction."""
        neighbors: list[CellCoordinates] = []
        for movement in Movements:
            potential_neighbor = self.get_neighbor_coords(coords, movement.value)
            if self.is_available(potential_neighbor) is False:
                continue
            if visited is not None and self.is_visited(potential_neighbor) is not visited:
                continue
            neighbors.append(potential_neighbor)
        return neighbors
    
    def break_wall(self, coords: CellCoordinates, neighbor: CellCoordinates) -> None:
        """Break down the wall between two cells. They must be directly adjacent to each other."""
        direction = Movements((neighbor[0] - coords[0]), (neighbor[1] - coords[1]))
        opposite = Movements(-(neighbor[0] - coords[0]), -(neighbor[1] - coords[1]))
        self.cells[coords[0]][coords[1]].walls[Directions[direction.name]] = False
        self.cells[neighbor[0]][neighbor[1]].walls[Directions[opposite.name]] = False

    def become_visited(self, coords: CellCoordinates) -> None:
        """Set the cell to is_visited = True."""
        self.cells[coords[0]][coords[1]].is_visited = True
    
    def path_to_unvisited(self, coords: CellCoordinates) -> CellCoordinates | None:
        """"""
        neighbors: list[CellCoordinates] = self.get_neighbors(coords, False)
        if neighbors == []:
            return None
        shuffle(neighbors)
        next_cell = neighbors[0]
        self.break_wall(coords, next_cell)
        self.become_visited(next_cell)
        return next_cell

    def dead_end_opener(self) -> None:
        """"""
        dead_end: list[CellCoordinates] = []
        for y in range(0, (self.config.HEIGHT)):
            for x in range(0, (self.config.WIDTH)):
                if sum(self.cells[x][y].walls) == 3:
                    dead_end.append((x, y))
        shuffle(dead_end)
        for coord in dead_end:
            direction: int = self.cells[coord[0]][coord[1]].walls.index(False)
            opposite: Movements = Movements((direction + 2) % 4)
            if self.is_neighbor_in_maze(coord, opposite, True) is False:
                continue
            self.open_wall(coord, opposite)
            break
        else:
            for coord in dead_end:
                direction: int = self.cells[
                    coord[0]][coord[1]].walls.index(False)
                for potential_turn in (1, 3):
                    turn: Movements = Movements(
                        (direction + potential_turn) % 4)

    def random_wall_breaker(self) -> None:
        """Method for breaking a wall. If there are three consecutive walls,
        the one in the middle has a 33% chance of being broken.
        """
        broken_wall: int = 0
        consecutive_wall: int = 0
        for y in range(0, (self.config.HEIGHT - 1)):
            for x in range(0, (self.config.WIDTH)):
                if self.cells[x][y].walls[1] is True:
                    consecutive_wall += 1
                    if consecutive_wall >= 3:
                        if randint(0, 100) < 70:
                            self.cells[x-1][y].walls[1] = False
                            self.cells[x-1][y+1].walls[3] = False
                            consecutive_wall = 1
                            broken_wall += 1
                else:
                    consecutive_wall = 0
        consecutive_wall = 0
        for x in range(0, (self.config.WIDTH - 1)):
            for y in range(0, (self.config.HEIGHT)):
                if self.cells[x][y].walls[2] is True:
                    consecutive_wall += 1
                    if consecutive_wall >= 3:
                        if randint(0, 100) < 70:
                            self.cells[x][y-1].walls[2] = False
                            self.cells[x+1][y-1].walls[0] = False
                            consecutive_wall = 1
                            broken_wall += 1
                else:
                    consecutive_wall = 0
        if broken_wall == 0:
            self.dead_end_opener()

    # _________________________________________________________________________
    #                                  ALGORITHMS
    # _________________________________________________________________________

    def backtracking_algo(self) -> Generator[None]:
        """Method to generate a perfect maze with a backtraking algorithm.
        Return a Generator to display a dynamic maze.
        """
        start: CellCoordinates = (randint(0, (self.config.WIDTH - 1)),
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
        """Method to generate a perfect maze with a Prim algorithm."""
        frontiers: set[CellCoordinates] = set()
        possibilities: list[tuple[int, int]] = list(
            move.value for move in Movements)
        starts: tuple[CellCoordinates, ...] = (
            (int((self.config.WIDTH - 1)/2), 0),
            (self.config.WIDTH - 1, int((self.config.HEIGHT - 1)/2)),
            (int((self.config.WIDTH - 1)/2), self.config.HEIGHT - 1),
            (0, int((self.config.HEIGHT - 1)/2)),
            (int((self.config.WIDTH - 1)/2), int((self.config.HEIGHT - 1)/2)))
        start: CellCoordinates = choice(starts)
        self.cells[start[0]][start[1]].is_visited = True

        def find_frontiers() -> None:
            """Method to find all frontier's cell."""
            for movement in possibilities:
                frontier_test: CellCoordinates = self.try_breaking_wall(
                    start, movement, False)
                if frontier_test == start:
                    continue
                else:
                    frontiers.add(frontier_test)

        maze_cell: list[CellCoordinates] = [start, start]
        find_frontiers()
        while frontiers:
            start = choice(list(frontiers))
            self.cells[start[0]][start[1]].is_visited = True
            frontiers.remove(start)
            maze_cell.append(start)
            for cell in reversed(maze_cell):
                direction: tuple[int, int] = (
                    cell[0] - start[0], cell[1] - start[1])
                if direction in Movements:
                    self.cells[cell[0]][cell[1]].walls[Directions[Movements(
                        (-direction[0], -direction[1])).name]] = False
                    self.cells[start[0]][start[1]].walls[Directions[Movements(
                        direction).name]] = False
                    break
            yield None
            find_frontiers()

    def generate_maze(self) -> None:
        self.generation(True)
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Backtracking": self.backtracking_algo,
            "Prim": self.prim_algo}
        for _ in algorithms[self.config.GEN_ALGORITHM]():
            pass
        if self.config.PERFECT is False:
            self.wall_breaker()

    def stepped_generation(self) -> Generator[None]:
        self.generation(True)
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Backtracking": self.backtracking_algo,
            "Prim": self.prim_algo}
        for _ in algorithms[self.config.GEN_ALGORITHM]():
            yield None
        if self.config.PERFECT is False:
            self.wall_breaker()

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
        width=12,
        height=12,
        entry=(0, 0),
        exit=(0, 1),
        perfect=True,
        gen_algorithm="Backtracking",
        seed=randint(0, 99999999),
        central_icon=False
    )
    print(maze.config)
    for _ in maze.stepped_generation():
        print("\033[3J\033[1;0H\033[0J")
        print(maze)
        sleep(0.01)
