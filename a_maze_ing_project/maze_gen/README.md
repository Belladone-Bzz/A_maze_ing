# A_maze_ing

## Maze_gen module

> [!NOTE]
> No AI was used in the making of this module nor README file. Documentation written by [Belladone-Bzz](https://github.com/Belladone-Bzz), changes updated by [Jolyne Mangeot](https://github.com/jolyne-mangeot)

This module manages all the classes, enumerations, methods and algorithms required to generate a maze, within the maze.py file.
This file can be found as a [Github Gist here](https://gist.github.com/Belladone-Bzz/98f3d80636ba63530c14b6fb08277536)

**Key features of our maze generator:**
- Several generation algorithms have been implemented. The dynamic display of these algorithms clearly illustrates the very different ways in which they generate a maze. The appearance of the final maze also varies depending on the algorithm chosen. We made this choice to highlight the diversity and complexity of the various existing algorithms
- We gave a great deal of thought to the generation of imperfect mazes. We could have simply broken down walls at random in our imperfect mazes to create loops. However, to make the imperfect mazes more aesthetically pleasing and avoid the creation of rooms, we employed several methods, giving out two distinct algorithms described below.
	- Firstly, we used a method that only breaks walls when there are at least three consecutive horizontal or vertical walls in a row; by breaking the one in the middle (with an 80% probability), this prevents the creation of rooms. In the case of small mazes, this method was not always feasible.
	- In such cases, all the dead ends in the maze were analysed. The priority was to break down the wall opposite the entrance to the dead end whenever possible. If this was not possible, we looked for a dead-end with two consecutive walls on at least one of its sides in order to break through a wall.
	- If this was still not feasible, only then would we randomly break through a side wall of a dead-end. This method has enabled us to minimise the generation of chambers, which only occur in rare cases in 3x3 mazes.

### maze.py

#### Enums:
- `Directions(IntEnum)`: Enum for WEST(0), SOUTH(1), EAST(2) and NORTH(3) directions.
- `Movements(Enum)`: Enum for:
	- west(-1, 0),
	- south(0, +1),
	- east(+1, 0),
	- north(0, -1).

	Each direction is associated with a tuple of x, y movements to go on in the given direction.

#### Classes:
- `Maze`: Class Maze.
	- **Utility:** Contain all classes, methods and algorithms used to generate a maze.
	- **Nested_class:** Cell.
	- **Attributes:**
		- <u>Maze Config Attributes:</u> width, height, entry, exit, perfect, gen_algorithm, imperfect_algorithm, pattern,
		- <u>Cell Matrix:</u> cells,
		- <u>Pattern Attributes:</u> pattern_h_offset, pattern_v_offset,
		- <u>Generation flags:</u> initialized, pattern_implemented, generated, imperfected.
	- **Methods:**
		- init, str, repr,
		- <u>Maze initialization:</u> grid_generation, integrate_pattern, add_enclosed_cells_to_pattern,
		- <u>Maze info getters:</u> get_cell, get_movement, get_neighbor_coord, get_neighbors, find_dead_end, is_available, is_in_maze,
		- <u>Generation utility:</u> break_wall, add_wall, add_to_maze, path_to_not_in_maze,
		- <u>Imperfect maze generation utility:</u> check_consec_walls, dead_end_opener, room_closer, break_random_wall,
		- <u>Generation algorithms:</u> backtracking_algo, prim_algo, hunt_and_kill_algo,
		- <u>Imperfect algorithms:</u> choke_points_algo, braided_algo,
		- <u>Maze generation triggers:</u> generate_maze, stepped_generation.

- `Cell`: Class Cell, nested in Maze class.
	- **Utility:** Allows you to instantiate, store and manipulate each cell in the grid.
	- **Attributes:** coordinates, walls, entry, exit, pattern, is_in_maze, is_visited.
	- **Methods:** init.

- `Config`: Class Config, nested in Maze class. Inherit from BaseModel from Pydantic module.
	- **Utility:** Check that the maze configuration given is correct.
	- **Attributes:** WIDTH, HEIGHT, ENTRY, EXIT, GEN_ALGORITHM, PATTERN, PERFECT, SEED.
	- **Methods:** validate_config, check_pattern.

- `GenerationError`: Custom Exception.
	- **Utility:** Custom exception raised at specific times if the maze generation steps have not been correctly called, which would result in unexpected errors.

	Otherwise raised in the single case scenario where the entry or exit coordinates are stuck inside the central pattern.

	- **Parameters:**
		- Maze object that has raised the error (to print with str or repr method)
		- msg, a string message containing a specialized notice on the exception
		that occured

#### Functions:

- **Maze grid and pattern:**
	- `grid_generation(self, walled: bool) -> None`: Method to generate all the cells in the maze grid in a list[list[Maze.Cell]] Only the outer walls are set to True. Entry and Exit cells are memorized.
	- `integrate_pattern(self) -> None`: Method that reads the given PATTERN and applies it to the current Maze, marking all concerned cells as pattern (attribute set to True), and marking up all their walls.
	- `add_enclosed_cells_to_pattern(self) -> None`: Method to add every cells that weren't visited by the generating algorithm to the pattern, so they won't be selected during the making of an imperfect maze. This concerns cells enclosed by the pattern but not part of its drawing.
- **Maze informations getters:**
	- `get_cell(self, cell: CellCoordinates) -> Cell`: Returns the Cell object present at the given coordinates. Raises an IndexError if the cell is outside the maze.
	- `get_movement(self, source: CellCoordinates, dest: CellCoordinates) -> Movements`: Get the movement to apply when moving from the source cell to the destination. Because it fetches it from the Movements enum, if the given cells aren't neighbors, it will raise an AttributeError.
	- `get_neighbor_coords(self, coords: CellCoordinates, movement: tuple[int, int]) -> CellCoordinates`: Return the coordinates of the neighbor of the given cell(coords), in the specified direction.
	- `get_neighbors(self, coords: CellCoordinates, in_maze: bool | None) -> list[CellCoordinates]`: Return a list of available neighbors. The list can be filtered to	include only neighbors that have been added to maze, those that aren't, or all of them without distinction.
	- `find_dead_end(self) -> list[CellCoordinates]`: Search all dead end in the maze, make a list of their coordinate and return it. Doesn't include dead-ends encased into the pattern.
	- `is_available(self, coords: CellCoordinates) -> bool`: Check that a cell is accessible: within the grid and not reserved for the central pattern.
	- `is_in_maze(self, coords: CellCoordinates) -> bool`: Check whether a cell is in the maze or not.
- **Generation utility:**
	- `break_wall(self, coords: CellCoordinates, neighbor: CellCoordinates) -> None`: Break down the wall between two cells. They must be directly adjacent to each other.
	- `add_wall(self, coords: CellCoordinates, neighbor: CellCoordinates) -> None`: Add up a wall between two cells. They must be directly adjacent to each other.
	- `add_to_maze(self, coords: CellCoordinates) -> None`: Set the cell to is_in_maze = True.
	- `path_to_unvisited(self, coords: CellCoordinates) -> CellCoordinates | None`: Find the neighbors of the cell with the coordinates passed as an argument. Break down the walls between that cell and one of its randomly selected neighbors. Return the coordinate of the new cell in the maze, or None if the initial cell has no neighbors.
- **Imperfect maze generation utility**
	- `check_consec_walls(self, axes: str) -> list[CellCoordinates]`: Check if a wall is part of a sequence of 3+ consecutive walls along the horizontal or vertical axes of the grid. If it's the case it has 80% chance to be added to the list of walls to be broken. Return the list of these walls.
	- `dead_end_opener(self) -> None`: Search dead end and make a path in an optimal way to avoid chambers in the maze. In order of priority: 1.Open the wall opposite the dead-end opening if the opposite cell is available. 2.Search for a dead-end with two True walls on the same side, perpendicular to the dead-end’s entrance, to avoid creating chambers. 3.If no dead-end meets these criteria, then a random dead-end is chosen and one of the walls perpendicular to the entrance is opened if the adjacent cell is available.
	- `room_closer(self) -> Generator[None]`: Detect 'rooms', areas where four cells aren't separated by any wall, and add a new wall randomly to ensure every hallway in the maze is only 1 cell large anywhere. Yields None every time a room is closed.
	- `break_random_wall(self) -> None`: Pick a dead-end from the dead-end list returned by the dedicated method, and break one of its side walls, because this method is only called after all dead-end have been remove by deleting their back wall. This is a fail-safe for the choke-points algorithm if the maze generation can't ensure the prevention of room creation within the maze.
- **Generation algorithms:**
	- `backtracking_algo(self) -> Generator[None]`: Generate a perfect maze with a backtraking algorithm. Return a Generator to display a dynamic maze.
	- `prim_algo(self) -> Generator[None]`: Generate a perfect maze with a Prim algorithm. Return a Generator to display a dynamic maze.
	- `hunt_and_kill_algo(self) -> Generator[None]`: Generate a perfect maze with a Hunt and Kill algorithm. Return a Generator to display a dynamic maze.
- **Imperfect maze generation algorithms**
	- `choke_points_algo(self) -> Generator[None]`: Turn a perfect maze into an imperfect one by breaking walls that are 3 cells long, ensuring no room are created. If no wall can be broken that way, open up a single dead-end with dead-end opener. Yields None when walls a broken.
	- `braided_algo(self) -> Generator[None]`: Imperfect algorithm which purpose is to open up loops within the maze by eliminating every dead-end. Loops through 3 actions until the only remaining dead-ends are caused by the pattern, ensuring no room is created in the process.
		- Open up dead-ends first through their back wall, then their side wall if their back wall leads outside the maze, sometimes creating rooms.
		- Open up the angles of the maze by moving the sidewall that's inside the maze inward, sometimes creating other dead-end.
		- Close down rooms by placing randomly a wall inside each of them, sometimes creating dead-ends. Loops and yields None for each action until no dead-end are to be found. Edge cases may generate infinite loops.
- **Maze generation and display:**
	- `generate_maze(self) -> Generator[None]`: Generate the maze with the algorithm given in config, and make it imperfect if perfect is set to False. The generation is done and the maze is display after it.
	- `stepped_generation(self) -> Generator[None]`: Generate the maze with the algorithm given in config, and make it imperfect if perfect is set to False. The display is done during the generation, making it dynamic.
