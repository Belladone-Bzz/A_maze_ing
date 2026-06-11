# A_maze_ing

## Maze_gen module

> [!NOTE]
> No AI was used in the making of this module nor README file. Documentation written by [Belladone-Bzz](https://github.com/Belladone-Bzz)

This module manages all the classes, enumerations, methods and algorithms required to generate a maze, within the maze.py file.
This file can be found as a [Github Gist here](https://gist.github.com/Belladone-Bzz/98f3d80636ba63530c14b6fb08277536)

**Key features of our maze generator:**
- Several generation algorithms have been implemented. The dynamic display of these algorithms clearly illustrates the very different ways in which they generate a maze. The appearance of the final maze also varies depending on the algorithm chosen. We made this choice to highlight the diversity and complexity of the various existing algorithms
- We gave a great deal of thought to the generation of imperfect mazes. We could have simply broken down walls at random in our imperfect mazes to create loops. However, to make the imperfect mazes more aesthetically pleasing and avoid the creation of rooms, we employed several methods. 
    - Firstly, we used a method that only breaks walls when there are at least three consecutive horizontal or vertical walls in a row; by breaking the one in the middle (with an 80% probability), this prevents the creation of rooms. In the case of small mazes, this method was not always feasible.
    - In such cases, all the dead ends in the maze were analysed. The priority was to break down the wall opposite the entrance to the dead end whenever possible. If this was not possible, we looked for a dead-end with two consecutive walls on at least one of its sides in order to break through a wall.
    - If this was still not feasible, only then would we randomly break through a side wall of a dead-end. This method has enabled us to minimise the generation of chambers, which only occur in rare cases in 3x3 mazes.

### maze.py

#### Enums:
- `Directions(IntEnum)`: Enum for WEST(0), SOUTH(1), EAST(2) and NORTH(3) directions.
- `Movements(Enum)`: Enum for WEST(-1, 0), SOUTH(0, +1), EAST(+1, 0) and NORTH(0, -1) movements. Each direction is associated with a tuple of x, y movements to go in the given direction.
  
#### Classes:
- `Maze`: Class Maze.
  - **Utility:** Contain all classes, methods and algorithms used to generate a maze.
  - **Nested_class:** Config, Cell.
  - **Attributes:** width, height, entry, exit, perfect, gen_algorithm, seed, pattern, config, cells.
  - **Methods:** init, integrate_pattern, add_enclosed_cells_to_pattern, grid_generation, get_neighbor_coord, is_available, is_in_maze, get_neighbors, break_wall, add_to_maze, path_to_unvisited, check_consec_walls, find_dead_end, dead_end_opener, backtracking_algo, prim_algo, hunt_and_kill_algo, make_maze_imperfect, generate_maze, stepped_generation, repr   

-  `Config`: Class Config, nested in Maze class. Inherit from BaseModel from Pydantic module.
   - **Utility:** Check that the maze configuration given is correct.
   - **Attributes:** WIDTH, HEIGHT, ENTRY, EXIT, GEN_ALGORITHM, PATTERN, PERFECT, SEED.
   - **Methods:** validate_config.

-  `Cell`: Class Cell, nested in Maze class.
   - **Utility:** Allows you to instantiate, store and manipulate each cell in the grid.
   - **Attributes:** coordinates, walls, entry, exit, pattern, is_in_maze.
   - **Methods:** init.

#### Functions:

- **Maze grid and pattern:**
  - `integrate_pattern(self) -> None`: Method that reads the given PATTERN and applies it to the current Maze, marking all concerned cells as pattern (attribute set to True), and marking up all their walls.
  - `add_enclosed_cells_to_pattern(self) -> None`: Method to add every cells that weren't visited by the generating algorithm to the pattern, so they won't be selected during the making of an imperfect maze. This concerns cells enclosed by the pattern but not part of its drawing.
  - `grid_generation(self, walled: bool) -> None`: Method to generate all the cells in the maze grid in a list[list[Maze.Cell]] Only the outer walls are set to True. Entry and Exit cells are memorized.
- **Generation utils:**
  - `get_neighbor_coords(self, coords: CellCoordinates, movement: tuple[int, int]) -> CellCoordinates`: Return the coordinates of the neighbor of the given cell(coords), in the specified direction.
  - `is_available(self, coords: CellCoordinates) -> bool`: Check that a cell is accessible: within the grid and not reserved for the central pattern.
  - `is_in_maze(self, coords: CellCoordinates) -> bool`: Check whether a cell is in the maze or not.
  - `get_neighbors(self, coords: CellCoordinates, in_maze: bool | None) -> list[CellCoordinates]`: Return a list of available neighbors. The list can be filtered to  include only neighbors that have been added to maze, those that aren't, or all of them without distinction.
  - `break_wall(self, coords: CellCoordinates, neighbor: CellCoordinates) -> None`: Break down the wall between two cells. They must be directly adjacent to each other.
  - `add_to_maze(self, coords: CellCoordinates) -> None`: Set the cell to is_in_maze = True.
  - `path_to_unvisited(self, coords: CellCoordinates) -> CellCoordinates | None`: Find the neighbors of the cell with the coordinates passed as an argument. Break down the walls between that cell and one of its randomly selected neighbors. Return the coordinate of the new cell in the maze, or None if the initial cell has no neighbors.
  - `check_consec_walls(self, axes: str) -> list[CellCoordinates]`: Check if a wall is part of a sequence of 3+ consecutive walls along the horizontal or vertical axes of the grid. If it's the case it has 80% chance to be added to the list of walls to be broken. Return the list of these walls.
  - `find_dead_end(self) -> list[CellCoordinates]`: Search all dead end in the maze, make a list of their coordinate and return it.
  - `dead_end_opener(self) -> None`: Search dead end and make a path in an optimal way to avoid chambers in the maze. In order of priority: 1.Open the wall opposite the dead-end opening if the opposite cell is available. 2.Search for a dead-end with two True walls on the same side, perpendicular to the dead-end’s entrance, to avoid creating chambers. 3.If no dead-end meets these criteria, then a random dead-end is chosen and one of the walls perpendicular to the entrance is opened if the adjacent cell is available.
- **Generation algorithms:**
  - `backtracking_algo(self) -> Generator[None]`: Generate a perfect maze with a backtraking algorithm. Return a Generator to display a dynamic maze.
  - `prim_algo(self) -> Generator[None]`: Generate a perfect maze with a Prim algorithm. Return a Generator to display a dynamic maze.
  - `hunt_and_kill_algo(self) -> Generator[None]`: Generate a perfect maze with a Hunt and Kill algorithm. Return a Generator to display a dynamic maze.
  - `make_maze_imperfect(self) -> Generator[None]`: Make an imperfect maze from a perfect one. Use check_consec_walls() method to have all the walls to broke. If there is none, use dead_end_opener() method.
- **Maze generation and display:**
  - `generate_maze(self) -> None`: Generate the maze with the algorithm given in config, and make it imperfect if perfect is set to False. The generation is done and the maze is display after it.
  - `stepped_generation(self) -> Generator[None]`: Generate the maze with the algorithm given in config, and make it imperfect if perfect is set to False. The display is done during the generation, making it dynamic.
  - `__repr__(self) -> str`: Method to display debug mode of the maze walls.
