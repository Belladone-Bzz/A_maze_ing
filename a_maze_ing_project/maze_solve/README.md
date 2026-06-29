# A_maze_ing

## Maze_solve module

> [!NOTE]
> No AI was used in the making of this module nor README file. Documentation written by [Belladone-Bzz](https://github.com/Belladone-Bzz)

This module manages all the classes, enumerations, methods and algorithms required to solve a maze, within the maze_solver.py file. Several resolution algorithms have been implemented: Dijkstra, dead end filler, breadth first search, and A* algorithms. We made this choice to highlight the diversity and complexity of the various existing algorithms.

This module contain MazeSolver and Node classes. FoudDeadEnd Exception. And all functions used to solve a perfect or imperfect maze.

This file can be found as a [Github Gist here](https://gist.github.com/Belladone-Bzz/909772387bbf47c46ae5931de904315e)

**Key features of our maze solver:**
Several solution algorithms have been implemented. The dynamic display of these algorithms clearly illustrates the very different ways in which they solve a maze. We made this choice to highlight the diversity and complexity of the various existing algorithms.
We have chosen these four algorithms:
- Dead-end filler
- Breadth first search
- Dijkstra
- A*

### maze_solver.py

#### Exception:
- `FoundDeadEnd(Exception)`: Exception to be raised by algorithms when finding a dead-end, useful for backtracking algorithms for example.

#### Classes:
- `MazeSolver`: Class MazeSolver.
  - **Utility:** Contain all classes, methods and algorithms used to solve a maze.
  - **Nested_class:** Node
  - **Attributes:** maze, entry, exit, highlighted (for display purposes), shortest_path and intersection_cells (graph utility).
  - **Methods:** init, record_maze_intersections, find_next_intersection, generate_cell_graph, set_all_nodes_distance_from_entry, calc_node_priority, set_priority_nodes_distance_from_entry, get_neighbour_nodes, create_neighbours_list, get_dist_from_entry, set_distance_from_entry, get_connected_neighbors, number_visited_neighbors, update_dead_end, find_path_to_exit, graph_algorithms, dead_end_filler, breadth_first_search_algorithm, stepped_maze_solving, maze_solving.

- `Node`: Class Node, nested if MazeSolver class.
  - **Utility:** Store additional informations about each cell of the Maze. In this graph implementation, each intersection cell holds these informations about each of their neighbours intersections. Helps navigating and saving traveling time.
  - **Attributes:** coords, distance, path

#### Functions:

- **GRAPH UTILITY:**
  - `record_maze_intersections(self) -> Generator[None]`: Loops through every cell of the Maze to append them to the intersection_cells set when they are surrounded by 0 or 1 wall, meaning they connect more than 3 cells. Separatly includes the entry and exit cells. Yields None each time a cell is added to the set for display purposes.
  - `find_next_intersection(self, cell: CellCoordinates, dir: Directions) -> Node`: Given a cell and a direction, connects to the first found intersection_cell and returns a Node object from the information found during navigation. Raise FoundDeadEnd error when hitting a wall. Automatically turns when the path winds.
  - `generate_cell_graph(self) -> Generator[None]`: Calls record_maze_intersections and find_next_intersection methods to instantiate the intersection_cells set and a Node object for each neighbour of an intersection that's inserted into a list added as attribute to Cell objects for future reference. Yields None from record_maze_intersections for display purposes.
  - `set_all_nodes_distance_from_entry(self) -> Generator[None]`: From the entry intersection, calculates the distance from it to each intersection of the Maze, saving the closest Node to access to go back to the entry the fastest. Stops when every Node is processed, and yields None when checking each Node distance for display purposes.
  - `calc_node_priority(self, node: CellCoordinates, dest: CellCoordinates) -> int`: Returns an int corresponding to the Manhattan distance as an absolute, to be used in priorizing the closest node from the destination.
  - `set_priority_nodes_distance_from_entry(self) -> Generator[None]`: From the entry intersection, calculates the distance from it to each intersection of the Maze, saving the closest Node to access to go back to the entry the fastest. Works with a priority queue to process the nodes with the lowest distance from the exit first. Stops when the exit point is processed, and yields None when checking each Node distance for display purposes.
  - `get_neighbour_nodes(self, cell: CellCoordinates) -> list[Node]`: Retrieve the neighbour_nodes Maze.Cell attribute given to intersection cells to keep track of where each node lead. This attribute contains a list of Node object.
  - `create_neighbours_list(self, cell: CellCoordinates) -> None`: Declare the neighbour_nodes attribute to a Cell and assign it an empty list. To be used for intersection cells to keep track of which other intersection they can lead to. The attribute is then destined to be a list of Node object.
  - `get_dist_from_entry(self, cell: CellCoordinates) -> tuple[int, tuple[CellCoordinates, ...]]`: Retrieve the distance_from_entry Maze.Cell attribute given to intersection cells to keep track of their distance from the entry cell. This attribute has to be declared using the MazeSolver method set_distance_from_entry with a value. It contains an int of traveled cells, as well as the path to take to reach the neighbouring node closest to the entry.
  - `set_distance_from_entry(self, cell: CellCoordinates, distance: tuple[int, tuple[CellCoordinates, ...] | None]) -> None`: Assign a value to the distance_from_entry Cell attribute. This value can be None in declaring purposes.

- **SOLVING UTILITY:**
  - `get_connected_neighbors(self, coords: CellCoordinates, in_maze: bool | None) -> list[CellCoordinates]`: Return a list of available neighbors. The list can be filtered to include only neighbors that have been added to maze, those that aren't, or all of them without distinction.
  - `number_visited_neighbors(self, coords: CellCoordinates) -> int`: Count the number of adjacent cells for which is_visited` is True. Returns this number.
  - `update_dead_end(self) -> list[CellCoordinates]`: Update dead ends for the dead_end_filler algorithm. Checks all cells in the grid. If they are is_visited = False and the sum of (walls + adjacent cells that are is_visited = True) equals 3, then they are added to the list of dead ends returned.
  - `find_path_to_exit(self) -> Generator[None]`: Find the path from the entry to the exit when all cells are marked as visited if out of the single path between the two cells.

- **ALGORITHMS:**
  - `graph_algorithms(self, algorithm: str) -> Generator[None]`: Finds the shortest path in the maze using a graph algorithm (Dijkstra or A-star). Sets a list of intersection_cells and calculate the distance between each to generate a weighted graph, including the entry and exit cells. Checks then each of their distance from the start, priorizing lighter distances, either until all paths are counted for or the exit is found. Goes back from the exit, adding to the shortest_path each path to take to go back an intersection that's the closest from the entry. Yields None at visually significant instants, updating the is_visited Cell attribute, highlighted and shortest_path MazeSolver attributes.
  - `dead_end_filler(self) -> Generator[None]`: Find the path from the entrance to the exit in a perfect maze. This dead-end detection algorithm identifies all the dead ends in the maze (excluding the entrance and exit if they are part of them). These cells are marked as `is_visited = True`. The dead ends are then updated in a loop, and the only cells remaining with `is_visited = False` are the path from the entrance to the exit. The algorithm then create a list of the cells that form the entrance-to-exit path.
  - `breadth_first_search_algorithm(self) -> Generator[None]`: Find the path from the entrance to the exit in a perfect or imperfect maze. This bfs algorithm explore all cells in the maze from the entry and stop as soon as it find the exit cell. These cells are marked as `is_visited = True`. The shortest path is memorized in the MazeSolver Class.

- **SOLVING GENERATION AND DISPLAY:**
  - `stepped_maze_solving(self) -> Generator[None]`: Triggers the solver's chosen algorithm to find a path in the maze between the entry and exit points. Yields None at pertinent times in display purposes.
  - `maze_solving(self) -> None`: Triggers the solver's chosen algorithm to find a path in the maze between the entry and exit points. Returns None.
