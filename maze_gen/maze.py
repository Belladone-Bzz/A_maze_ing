from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated
from enum import IntEnum, Enum
from random import seed as set_seed, choice, randint, shuffle


MazeDimension = Annotated[int, Field(ge=2)]
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
            perfect: bool, seed: int, central_icon: bool = False):
        self.config = Maze.Config(
            WIDTH=width,
            HEIGHT=height,
            ENTRY=entry,
            EXIT=exit,
            PERFECT=perfect,
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
            if self.ENTRY[0] >= self.HEIGHT or self.ENTRY[1] >= self.WIDTH:
                error_message += (
                    "Entry coordinates (x, y) "
                    "cannot exceed the maze's dimensions")
            if self.EXIT[0] >= self.HEIGHT or self.EXIT[1] >= self.WIDTH:
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

    def generation(self) -> None:
        """Method to generate all the cells in the maze grid in a
        list[list[Maze.Cell]] Only the outer walls are set to True.
        Entry and Exit cells are memorized.
         """
        for x in range(self.config.WIDTH):
            self.cells.append([])
            for y in range(self.config.HEIGHT):
                self.cells[x].append(Maze.Cell((x, y), True))
        for cell in self.cells[0]:
            cell.walls[Directions.WEST] = True
        for cell in self.cells[-1]:
            cell.walls[Directions.EAST] = True
        for x in range(self.config.WIDTH):
            self.cells[x][0].walls[Directions.NORTH] = True
            self.cells[x][-1].walls[Directions.SOUTH] = True
        self.cells[self.config.ENTRY[0]][self.config.ENTRY[1]].entry = True
        self.cells[self.config.EXIT[0]][self.config.EXIT[1]].exit = True

    def access_next_cell(self, coords:CellCoordinates) -> CellCoordinates:
        possibilities: list[tuple[int, int]] =\
            list(move.value for move in Movements)
        shuffle(possibilities)
        for x, y in possibilities:
            potential_coords: CellCoordinates = (
                coords[0] + x, coords[1] + y)
            if potential_coords[0] < 0 or potential_coords[1] < 0\
                or potential_coords[0] >= self.config.WIDTH\
                    or potential_coords[1] >= self.config.HEIGHT:
                continue
            if self.cells[potential_coords[0]]\
                    [potential_coords[1]].is_visited is False\
                    and self.cells[potential_coords[0]]\
                        [potential_coords[1]].pattern is False:
                self.cells[potential_coords[0]][potential_coords[1]].is_visited = True
                self.cells[coords[0]][coords[1]].walls[Directions[Movements((x, y)).name]] = False
                self.cells[potential_coords[0]][potential_coords[1]].walls[Directions[Movements((-x, -y)).name]] = False
                return potential_coords
        else:
            return coords

    def backtracking_algo(self) -> None:
        """Method to generate a perfect maze with a backtraking algorithm."""
        start: CellCoordinates = (randint(0, self.config.WIDTH),
                                  randint(0, self.config.HEIGHT))
        print(start)
        self.cells[start[0]][start[1]].is_visited = True
        current: CellCoordinates = self.access_next_cell(start) 
        back_track: list[CellCoordinates] = [start, current]
        while current != start:
            next_cell = self.access_next_cell(current)
            print(current, next_cell)
            if current != next_cell:
                current = next_cell
                back_track.append(current)
                continue
            else:
                current = back_track[-2]
                del back_track[-1]

    def prim_algo(self) -> None:
        """Method to generate a perfect maze with a Prim algorithm."""
        start: CellCoordinates = (randint(0, self.config.WIDTH),
                                  randint(0, self.config.HEIGHT))
        self.cells[start[0]][start[1]].is_visited = True
        maze_cell: list[CellCoordinates] = [start, start]
        frontiers: set[CellCoordinates] = set()
        possibilities: list[tuple[int, int]] =\
            list(move.value for move in Movements)
        for x, y in possibilities:
            potential_frontier: CellCoordinates = (
                start[0] + x, start[1] + y)
            if potential_frontier[0] < 0 or potential_frontier[1] < 0\
                or potential_frontier[0] >= self.config.WIDTH\
                    or potential_frontier[1] >= self.config.HEIGHT:
                continue
            if self.cells[potential_frontier[0]]\
                    [potential_frontier[1]].is_visited is False\
                    and self.cells[potential_frontier[0]]\
                        [potential_frontier[1]].pattern is False:
                frontiers.add(potential_frontier)
        while frontiers:
            print(start)
            start = choice(list(frontiers))
            self.cells[start[0]][start[1]].is_visited = True
            frontiers.remove(start)
            maze_cell.append(start)

            for cell in reversed(maze_cell):
                direction: tuple[int, int] = (cell[0] - start[0], cell[1] - start[1])
                if direction in Movements:
                    self.cells[cell[0]][cell[1]].walls[Directions[Movements((-direction[0], -direction[1])).name]] = False
                    self.cells[start[0]][start[1]].walls[Directions[Movements(direction).name]] = False
                    break


            for x, y in possibilities:
                potential_frontier = (
                    start[0] + x, start[1] + y)
                if potential_frontier[0] < 0 or potential_frontier[1] < 0\
                    or potential_frontier[0] >= self.config.WIDTH\
                        or potential_frontier[1] >= self.config.HEIGHT:
                    continue
                if self.cells[potential_frontier[0]]\
                        [potential_frontier[1]].is_visited is False\
                        and self.cells[potential_frontier[0]]\
                            [potential_frontier[1]].pattern is False:
                    frontiers.add(potential_frontier)
            
            print(frontiers)

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
    maze = Maze(
        width=20,
        height=20,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=666,
        central_icon=False
    )
    print(maze.config)
    maze.generation()
    print(maze)
    maze.prim_algo()
    print(maze)
