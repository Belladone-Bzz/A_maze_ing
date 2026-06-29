"""This module manages all the classes, enumerations, methods and algorithms
required to solve a maze, within the maze_solver.py file. Several resolution
algorithms have been implemented: Dijkstra, dead end filler, breadth first
search, and A* algorithms. We made this choice to highlight the diversity and
complexity of the various existing algorithms.

This module contain MazeSolver and Node classes. FoudDeadEnd Exception. And
all functions used to solve a perfect or imperfect maze.
"""

from typing import Generator, cast
from heapq import heappush, heappop
from functools import partial
from collections import deque
from collections.abc import Callable
from a_maze_ing_project.maze_gen.mazegenerator import (
    Maze, Directions, Movements, CellCoordinates)


class FoundDeadEnd(Exception):
    """Exception to be raised by algorithms when finding a dead-end, useful
    for backtracking algorithms for example.
    """
    pass


class MazeSolver:
    """Class containing all methods related to the solving of a Maze object
    by finding its shortest path from entry to exit. Integrates graph-creating
    methods for the Dijkstra algorithm and mostly works with the Maze-nested
    class Cell for navigating.

    Attributes: maze, highlighted (for display purposes), shortest_path and
    intersection_cells (graph utility).
    Notable algorithm methods: dijkstra_algorithm(), dead_end_filler(),
    stepped_maze_solving(algo: str) and maze_solving(algo: str) which are
    essentially the same except for stepped which is a Generator that yields
    None during key moment of the solving.
    """
    solving_algorithms: tuple[str, ...] = (
        "Dijkstra", "Dead_end_filler", "A_star", "Breadth_search")

    def __init__(
            self, maze: Maze, entry: CellCoordinates, exit: CellCoordinates,
            algorithm: str) -> None:
        self.maze: Maze = maze
        self.ENTRY: CellCoordinates = entry
        self.EXIT: CellCoordinates = exit

        self.algorithm: str = algorithm

        self.highlighted: tuple[CellCoordinates, ...] = ()
        self.shortest_path: list[CellCoordinates] = []

        self.intersection_cells: set[CellCoordinates]

    # _________________________________________________________________________
    #                         GRAPHS UTILITY
    # _________________________________________________________________________

    class Node:
        """Nested class to store additional informations about each cell
        of the Maze. In this graph implementation, each intersection cell
        holds these informations about each of their neighbours intersections.
        Helps navigating and saving traveling time.

        Attributes: coords: CellCoordinates, distance: int, path:
        tuple[CellCoordinates].
        """
        def __init__(
                self, coords: CellCoordinates, distance: int,
                path: tuple[CellCoordinates, ...]) -> None:
            self.coords: CellCoordinates = coords
            self.distance: int = distance
            self.path: tuple[CellCoordinates, ...] = path

    def record_maze_intersections(self) -> Generator[None]:
        """Loops through every cell of the Maze to append them to the
        intersection_cells set when they are surrounded by 0 or 1 wall,
        meaning they connect more than 3 cells. Separatly includes the entry
        and exit cells. Yields None each time a cell is added to the set for
        display purposes.
        """
        self.intersection_cells = {
            self.ENTRY, self.EXIT}
        self.create_neighbours_list(self.ENTRY)
        self.set_distance_from_entry(self.ENTRY, (0, None))
        self.maze.cells[self.ENTRY[0]][self.ENTRY[1]].is_visited = True
        self.create_neighbours_list(self.EXIT)
        self.set_distance_from_entry(self.EXIT, (-1, None))
        self.maze.cells[self.EXIT[0]][self.EXIT[1]].is_visited = True
        for x in range(self.maze.config.WIDTH):
            for y in range(self.maze.config.HEIGHT):
                if sum(self.maze.cells[x][y].walls) <= 1:
                    self.intersection_cells.add((x, y))
                    self.maze.cells[x][y].is_visited = True
                    self.set_distance_from_entry((x, y), (-1, None))
                    self.create_neighbours_list((x, y))
                    yield None

    def find_next_intersection(
            self, cell: CellCoordinates, dir: Directions
            ) -> Node:
        """Given a cell and a direction, connects to the first found
        intersection_cell and returns a Node object from the information found
        during navigation. Raise FoundDeadEnd error when hitting a wall.
        Automatically turns when the path winds.
        """
        temp_x: int
        temp_y: int
        x: int = cell[0]
        y: int = cell[1]
        distance_bet_cells: int = 1
        temp_x, temp_y = self.maze.get_neighbor_coords(
            (x, y), Movements[dir.name].value)
        route_taken: list[CellCoordinates] = [(temp_x, temp_y)]
        while (temp_x, temp_y) not in self.intersection_cells:
            if self.maze.cells[temp_x][temp_y].walls[dir] is False:
                pass
            elif self.maze.cells[temp_x][temp_y].walls[(dir + 1) % 4]\
                    is False:
                dir = Directions((dir + 1) % 4)
            elif self.maze.cells[temp_x][temp_y].walls[(dir + 3) % 4]\
                    is False:
                dir = Directions((dir + 3) % 4)
            else:
                raise FoundDeadEnd
            temp_x, temp_y = self.maze.get_neighbor_coords(
                (temp_x, temp_y), Movements[dir.name].value)
            distance_bet_cells += 1
            route_taken.append((temp_x, temp_y))
        return MazeSolver.Node(
            (temp_x, temp_y), distance_bet_cells, tuple(route_taken))

    def generate_cell_graph(self) -> Generator[None]:
        """Calls record_maze_intersections and find_next_intersection methods
        to instantiate the intersection_cells set and a Node object for each
        neighbour of an intersection that's inserted into a list added as
        attribute to Cell objects for future reference. Yields None
        from record_maze_intersections for display purposes.
        """
        for _ in self.record_maze_intersections():
            yield None
        found_node: MazeSolver.Node
        for x, y in self.intersection_cells:
            for direction in filter(
                    lambda dir: not self.maze.cells[x][y].walls[dir],
                    Directions):
                try:
                    found_node = (
                        self.find_next_intersection((x, y), direction))
                except FoundDeadEnd:
                    continue
                if found_node.coords == (x, y):
                    continue
                for neighbour in self.get_neighbour_nodes((x, y)):
                    if neighbour.coords == found_node.coords:
                        if found_node.distance < neighbour.distance:
                            neighbour.distance = found_node.distance
                            neighbour.path = found_node.path
                        break
                else:
                    self.get_neighbour_nodes((x, y)).append(found_node)

    def set_all_nodes_distance_from_entry(self) -> Generator[None]:
        """From the entry intersection, calculates the distance from it
        to each intersection of the Maze, saving the closest Node to access
        to go back to the entry the fastest. Stops when every Node is
        processed, and yields None when checking each Node distance for
        display purposes.
        """
        known_nodes: list[CellCoordinates] = [self.ENTRY]
        distance_from_entry: float
        entry_to_next_node: float
        current_node: CellCoordinates
        while len(known_nodes) > 0:
            current_node = known_nodes.pop(0)
            for next_node in self.get_neighbour_nodes(current_node):
                distance_from_entry = self.get_dist_from_entry(
                    next_node.coords)[0]
                entry_to_next_node = (
                    self.get_dist_from_entry(current_node)[0]
                    + next_node.distance)
                if (distance_from_entry == -1
                        or distance_from_entry > entry_to_next_node):
                    self.highlighted = next_node.path
                    self.set_distance_from_entry(
                        next_node.coords, (
                            entry_to_next_node,
                            tuple([current_node, *next_node.path][-2::-1])))
                    known_nodes.append(next_node.coords)
                    yield None
        self.highlighted = ()

    def calc_node_priority(
            self, node: CellCoordinates, dest: CellCoordinates) -> int:
        """Returns an int corresponding to the Manhattan distance as an
        absolute, to be used in priorizing the closest node from the
        destination.
        """
        return abs(node[0] - dest[0]) + abs(node[1] - dest[1])

    def set_priority_nodes_distance_from_entry(self) -> Generator[None]:
        """From the entry intersection, calculates the distance from it
        to each intersection of the Maze, saving the closest Node to access
        to go back to the entry the fastest. Works with a priority queue
        to process the nodes with the lowest distance from the exit first.

        Stops when the exit point is processed, and yields None when checking
        each Node distance for display purposes.
        """
        known_nodes: list[tuple[int, CellCoordinates]] = []
        heappush(known_nodes, (0, self.ENTRY))
        distance_from_entry: float
        entry_to_next_node: float
        current_node: CellCoordinates
        while len(known_nodes) > 0:
            current_node = heappop(known_nodes)[1]
            if current_node == self.EXIT:
                break
            for next_node in self.get_neighbour_nodes(current_node):
                distance_from_entry = self.get_dist_from_entry(
                    next_node.coords)[0]
                entry_to_next_node = (
                    self.get_dist_from_entry(current_node)[0]
                    + next_node.distance)
                if (distance_from_entry == -1
                        or distance_from_entry > entry_to_next_node):
                    self.highlighted = next_node.path
                    self.set_distance_from_entry(
                        next_node.coords, (
                            entry_to_next_node,
                            tuple([current_node, *next_node.path][-2::-1])))
                    heappush(
                        known_nodes, (
                            self.calc_node_priority(
                                next_node.coords, self.EXIT),
                            next_node.coords))
                    yield None
        self.highlighted = ()

    def get_neighbour_nodes(
            self, cell: CellCoordinates) -> list[Node]:
        """Retrieve the neighbour_nodes Maze.Cell attribute given to
        intersection cells to keep track of where each node lead. This
        attribute contains a list of Node object.
        """
        return cast(list[MazeSolver.Node], getattr(
            self.maze.cells[cell[0]][cell[1]], "neighbour_nodes"))

    def create_neighbours_list(self, cell: CellCoordinates) -> None:
        """Declare the neighbour_nodes attribute to a Cell and assign it
        an empty list. To be used for intersection cells to keep track of
        which other intersection they can lead to. The attribute is then
        destined to be a list of Node object.
        """
        setattr(
            self.maze.cells[cell[0]][cell[1]], "neighbour_nodes", [])

    def get_dist_from_entry(
            self, cell: CellCoordinates
            ) -> tuple[int, tuple[CellCoordinates, ...]]:
        """Retrieve the distance_from_entry Maze.Cell attribute given to
        intersection cells to keep track of their distance from the entry
        cell. This attribute has to be declared using the MazeSolver method
        set_distance_from_entry with a value.

        It contains an int of traveled cells, as well as the path
        to take to reach the neighbouring node closest to the entry.
        """
        return cast(tuple[int, tuple[CellCoordinates, ...]], getattr(
            self.maze.cells[cell[0]][cell[1]], "distance_from_entry"))

    def set_distance_from_entry(
            self, cell: CellCoordinates,
            distance: tuple[int, tuple[CellCoordinates, ...] | None]) -> None:
        """Assign a value to the distance_from_entry Cell attribute. This
        value can be None in declaring purposes.
        """
        setattr(
            self.maze.cells[cell[0]][cell[1]], "distance_from_entry", distance)

    # _________________________________________________________________________
    #                             SOLVING UTILS
    # _________________________________________________________________________

    def get_connected_neighbors(
            self, coords: CellCoordinates,
            in_maze: bool | None) -> list[CellCoordinates]:
        """Return a list of available neighbors. The list can be filtered to
        include only neighbors that have been added to maze, those that aren't,
        or all of them without distinction.
        """
        neighbors: list[CellCoordinates] = []
        for movement in Movements:
            potential_neighbor = self.maze.get_neighbor_coords(
                coords, movement.value)
            if self.maze.is_available(potential_neighbor) is False:
                continue
            if self.maze.cells[
                    potential_neighbor[0]][
                        potential_neighbor[1]].is_visited is True:
                continue
            if (in_maze is not None
                    and self.maze.is_in_maze(potential_neighbor)
                    is not in_maze):
                continue
            if (self.maze.cells[coords[0]][coords[1]].walls[
                    Directions[movement.name]] is True):
                continue
            neighbors.append(potential_neighbor)
        return neighbors

    def number_visited_neighbors(self, coords: CellCoordinates) -> int:
        """Count the number of adjacent cells for which is_visited` is
        True. Returns this number.
        """
        visited_neighbor: int = 0
        for movement in Movements:
            neighbor = self.maze.get_neighbor_coords(
                        coords, movement.value)
            if self.maze.is_available(neighbor) is False:
                continue
            if (self.maze.cells[neighbor[0]][neighbor[1]].is_visited
                    and self.maze.cells[coords[0]][coords[1]].walls[
                        Directions[movement.name]] is False):
                visited_neighbor += 1
        return visited_neighbor

    def update_dead_end(self) -> list[CellCoordinates]:
        """Update dead ends for the dead_end_filler algorithm. Checks all
        cells in the grid. If they are is_visited = False and the sum of
        (walls + adjacent cells that are is_visited = True) equals 3, then
        they are added to the list of dead ends returned.
        """
        dead_end: list[CellCoordinates] = []
        for y in range(0, (self.maze.config.HEIGHT)):
            for x in range(0, (self.maze.config.WIDTH)):
                if self.maze.cells[x][y].is_visited is True:
                    continue
                visited_neighbors: int = self.number_visited_neighbors((x, y))
                if (self.maze.cells[x][y].entry is True
                        or self.maze.cells[x][y].exit is True):
                    continue
                if sum(self.maze.cells[x][y].walls) + visited_neighbors == 3:
                    dead_end.append((x, y))
        return dead_end

    def find_path_to_exit(self) -> Generator[None]:
        """Find the path from the entry to the exit when all cells are marked
        as visited if out of the single path between the two cells.
        """
        self.shortest_path = [self.ENTRY]
        current: CellCoordinates = self.ENTRY
        while current != self.EXIT:
            for movement in Movements:
                neighbor = self.maze.get_neighbor_coords(
                            current, movement.value)
                if (len(self.shortest_path) > 1
                        and neighbor == self.shortest_path[-2]):
                    continue
                if self.maze.is_available(neighbor) is False:
                    continue
                if (self.maze.cells[
                        neighbor[0]][neighbor[1]].is_visited is False
                        and self.maze.cells[current[0]][current[1]].walls[
                            Directions[movement.name]] is False):
                    self.shortest_path.append(neighbor)
                    current = neighbor
                    yield None
                    break

    # _________________________________________________________________________
    #                              ALGORITHMS
    # _________________________________________________________________________

    def graph_algorithms(self, algorithm: str) -> Generator[None]:
        """Finds the shortest path in the maze using a graph algorithm
        (Dijkstra or A-star).
        Sets a list of intersection_cells and calculate the distance between
        each to generate a weighted graph, including the entry and exit
        cells. Checks then each of their distance from the start,
        priorizing lighter distances, either until all paths are counted for
        or the exit is found.

        Goes back from the exit, adding to the shortest_path each path to take
        to go back an intersection that's the closest from the entry.

        Yields None at visually significant instants, updating the is_visited
        Cell attribute, highlighted and shortest_path MazeSolver attributes.
        """
        for _ in self.generate_cell_graph():
            yield None
        if algorithm == "Dijkstra":
            for _ in self.set_all_nodes_distance_from_entry():
                yield None
        else:
            for _ in self.set_priority_nodes_distance_from_entry():
                yield None
        path_queue: deque[CellCoordinates] = deque([self.EXIT])
        while self.ENTRY != path_queue[0]:
            path_queue.extendleft(self.get_dist_from_entry(
                path_queue[0])[1])
            self.shortest_path = list(path_queue)
            yield None

    def dead_end_filler(self) -> Generator[None]:
        """Find the path from the entrance to the exit in a perfect maze. This
        dead-end detection algorithm identifies all the dead ends in the maze
        (excluding the entrance and exit if they are part of them). These cells
        are marked as `is_visited = True`. The dead ends are then updated in a
        loop, and the only cells remaining with `is_visited = False` are the
        path from the entrance to the exit. The algorithm then create a list
        of the cells that form the entrance-to-exit path.
        """
        if self.maze.config.PERFECT is False:
            print("Dead end filler algorithm can only be used for perfect"
                  "mazes.")
            return
        dead_end: list[CellCoordinates] = []
        dead_end = self.maze.find_dead_end()
        if self.ENTRY in dead_end:
            dead_end.remove(self.ENTRY)
        if self.EXIT in dead_end:
            dead_end.remove(self.EXIT)
        while dead_end != []:
            for cell in dead_end:
                self.maze.cells[cell[0]][cell[1]].is_visited = True
                yield None
            dead_end = self.update_dead_end()
        for _ in self.find_path_to_exit():
            yield None

    def breadth_first_search_algorithm(self) -> Generator[None]:
        """Find the path from the entrance to the exit in a perfect or
        imperfect maze. This bfs algorithm explore all cells in the maze from
        the entry and stop as soon as it find the exit cell. These cells
        are marked as `is_visited = True`. The shortest path is memorized in
        the MazeSolver Class.
        """
        known_cells: list[CellCoordinates] = [self.ENTRY]
        setattr(self.maze.cells[
            self.ENTRY[0]][self.ENTRY[1]], "prev_cell", self.ENTRY)
        self.maze.cells[self.ENTRY[0]][self.ENTRY[1]].is_visited = True
        while known_cells:
            self.highlighted = tuple(known_cells)
            cell = known_cells.pop(0)
            if cell == self.EXIT:
                break
            frontiers: list[CellCoordinates] = self.get_connected_neighbors(
                cell, True)
            for frontier in frontiers:
                try:
                    getattr(self.maze.cells[
                        frontier[0]][frontier[1]], "prev_cell")
                except AttributeError:
                    setattr(self.maze.cells[frontier[0]][
                        frontier[1]], "prev_cell", (cell[0], cell[1]))
                    self.maze.cells[frontier[0]][frontier[1]].is_visited = True
                    known_cells.append(frontier)
                    yield None
        self.highlighted = ()
        self.shortest_path = [self.EXIT]
        while self.ENTRY != self.shortest_path[0]:
            self.shortest_path.insert(
                0,
                getattr(self.maze.cells[self.shortest_path[0][0]][
                    self.shortest_path[0][1]], "prev_cell"))
            yield None

    # _________________________________________________________________________
    #                      SOLVING GENERATION AND DISPLAY
    # _________________________________________________________________________

    def stepped_maze_solving(self) -> Generator[None]:
        """Triggers the solver's chosen algorithm to find a path in the maze
        between the entry and exit points. Yields None at pertinent times
        in display purposes.
        """
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Dijkstra": partial(self.graph_algorithms, "Dijkstra"),
            "A_star": partial(self.graph_algorithms, "A_star"),
            "Breadth_search": self.breadth_first_search_algorithm,
            "Dead_end_filler": self.dead_end_filler}
        for _ in algorithms[self.algorithm]():
            yield None

    def maze_solving(self) -> None:
        """Triggers the solver's chosen algorithm to find a path in the maze
        between the entry and exit points.

        Returns None.
        """
        algorithms: dict[str, Callable[[], Generator[None]]] = {
            "Dijkstra": partial(self.graph_algorithms, "Dijkstra"),
            "A_star": partial(self.graph_algorithms, "A_star"),
            "Breadth_search": self.breadth_first_search_algorithm,
            "Dead_end_filler": self.dead_end_filler}
        for _ in algorithms[self.algorithm]():
            pass


if __name__ == "__main__":
    """If you encounter an ImportError on maze_gen when running this test
    file, run `pip install -e .` from the root of the repository. It will
    index every source file in an 'egg-info' folder and correct the path
    finding errors.
    """

    from random import randint

    maze: Maze = Maze(
        width=5,
        height=5,
        entry=(0, 0),
        exit=(4, 1),
        perfect=True,
        gen_algorithm="Prim",
        seed=randint(0, 99999999),
        pattern=[])
    maze.generate_maze()
    print(maze)
    print(maze.config.SEED)
    solv: MazeSolver = MazeSolver(
        maze, maze.config.ENTRY, maze.config.EXIT, "A_star")
    for _ in solv.breadth_first_search_algorithm():
        pass

    print("Solutions found:")
    print(solv.shortest_path)
