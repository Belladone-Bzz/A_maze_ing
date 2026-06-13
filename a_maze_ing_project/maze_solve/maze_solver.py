
from typing import cast
from a_maze_ing_project.maze_gen import (
    Maze, Directions, Movements, CellCoordinates)


class FoundDeadEnd(Exception):
    pass


class MazeSolver:
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.ENTRY: CellCoordinates = maze.config.ENTRY
        self.EXIT: CellCoordinates = maze.config.EXIT

        self.shortest_path: list[CellCoordinates]
        self.shortest_paths: list[list[CellCoordinates]]
        self.solutions: list[list[CellCoordinates]]

        self.intersection_cells: set[CellCoordinates]

    # _________________________________________________________________________
    #                         GRAPHS UTILITY
    # _________________________________________________________________________

    class Node:
        def __init__(
                self, coords: CellCoordinates, distance: int,
                path: tuple[CellCoordinates, ...]) -> None:
            self.coords: CellCoordinates = coords
            self.distance: int = distance
            self.path: tuple[CellCoordinates, ...] = path
            self.distance_from_entry: int = -1

    def record_maze_intersections(self) -> None:
        self.intersection_cells = {
            maze.config.ENTRY, maze.config.EXIT}
        self.create_neighbours_list(maze.config.ENTRY)
        self.set_distance_from_entry(maze.config.ENTRY, 0)
        self.create_neighbours_list(maze.config.EXIT)
        self.set_distance_from_entry(maze.config.EXIT, -1)
        for x in range(maze.config.WIDTH):
            for y in range(maze.config.HEIGHT):
                if sum(maze.cells[x][y].walls) <= 1:
                    self.intersection_cells.add((x, y))
                    self.set_distance_from_entry((x, y), -1)
                    self.create_neighbours_list((x, y))

    def find_next_intersection(
            self, cell: CellCoordinates, dir: Directions
            ) -> Node:
        maze: Maze = self.maze
        temp_x: int
        temp_y: int
        x: int = cell[0]
        y: int = cell[1]
        distance_bet_cells: int = 1
        temp_x, temp_y = maze.get_neighbor_coords(
            (x, y), Movements[dir.name].value)
        route_taken: list[CellCoordinates] = [(temp_x, temp_y)]
        while (temp_x, temp_y) not in self.intersection_cells:
            if maze.cells[temp_x][temp_y].walls[dir] is False:
                pass
            elif maze.cells[temp_x][temp_y].walls[(dir + 1) % 4]\
                    is False:
                dir = Directions((dir + 1) % 4)
            elif maze.cells[temp_x][temp_y].walls[(dir + 3) % 4]\
                    is False:
                dir = Directions((dir + 3) % 4)
            else:
                raise FoundDeadEnd
            temp_x, temp_y = maze.get_neighbor_coords(
                (temp_x, temp_y), Movements[dir.name].value)
            distance_bet_cells += 1
            route_taken.append((temp_x, temp_y))
        return MazeSolver.Node(
            (temp_x, temp_y), distance_bet_cells, tuple(route_taken))

    def generate_cell_graph(self) -> None:
        maze: Maze = self.maze
        found_node: MazeSolver.Node
        self.record_maze_intersections()
        for x, y in self.intersection_cells:
            for direction in filter(
                    lambda dir: not maze.cells[x][y].walls[dir], Directions):
                try:
                    found_node = (
                        self.find_next_intersection((x, y), direction))
                except FoundDeadEnd:
                    continue
                if found_node.coords is not (x, y):
                    for neighbour in self.get_neighbour_nodes((x, y)):
                        if (
                                neighbour.coords == found_node.coords
                                and neighbour.distance > found_node.distance):
                            neighbour.distance = found_node.distance
                            neighbour.path = found_node.path
                            break
                    else:
                        self.get_neighbour_nodes((x, y)).append(found_node)

    def set_nodes_distance_from_entry(self) -> None:
        processed_nodes: list[CellCoordinates] = [self.maze.config.ENTRY]
        temp_neighbours: list[CellCoordinates] = []
        distance_from_entry: float
        entry_to_next_node: float
        while any(
                self.get_dist_from_entry(cell) == -1
                for cell in self.intersection_cells) is True:
            for known_node in processed_nodes:
                for next_node in self.get_neighbour_nodes(known_node):
                    entry_to_next_node = (
                        self.get_dist_from_entry(known_node)
                        + next_node.distance)
                    distance_from_entry = self.get_dist_from_entry(
                        next_node.coords)
                    if (distance_from_entry == -1
                            or distance_from_entry > entry_to_next_node):
                        self.set_distance_from_entry(
                            next_node.coords, entry_to_next_node)
                    temp_neighbours.append(next_node.coords)
            processed_nodes = temp_neighbours
            temp_neighbours = []

    def get_neighbour_nodes(
            self, cell: CellCoordinates) -> list[Node]:
        return cast(list[MazeSolver.Node], getattr(
            self.maze.cells[cell[0]][cell[1]], "neighbour_nodes"))

    def create_neighbours_list(self, cell: CellCoordinates) -> None:
        setattr(
            self.maze.cells[cell[0]][cell[1]], "neighbour_nodes", [])

    def get_dist_from_entry(self, cell: CellCoordinates) -> float:
        return cast(float, getattr(
            self.maze.cells[cell[0]][cell[1]], "distance_from_entry"))

    def set_distance_from_entry(
            self, cell: CellCoordinates, value: float) -> None:
        setattr(
            self.maze.cells[cell[0]][cell[1]], "distance_from_entry", value)

    # _________________________________________________________________________
    #                         DIJKSTRA'S ALGORITHM
    # _________________________________________________________________________

    def dijkstra_algorithm(self) -> None:
        self.generate_cell_graph()
        self.set_nodes_distance_from_entry()
        self.shortest_paths = [[self.maze.config.EXIT]]
        neighbours: list[MazeSolver.Node]
        min_dist_to_entry: MazeSolver.Node
        while all(
                self.maze.config.ENTRY in path
                for path in self.shortest_paths) is False:
            for current_solution in filter(
                    lambda path: self.maze.config.ENTRY not in path,
                    self.shortest_paths):
                neighbours = self.get_neighbour_nodes(current_solution[-1])
                min_dist_to_entry = min(
                    neighbours,
                    key=lambda neigh: self.get_dist_from_entry(neigh.coords))
                for close_node in filter(
                        (
                            lambda node: self.get_dist_from_entry(node.coords)
                            == self.get_dist_from_entry(
                                min_dist_to_entry.coords)
                            and node.coords != min_dist_to_entry.coords),
                        neighbours):
                    self.shortest_paths.append(current_solution.copy())
                    self.shortest_paths[-1].extend(close_node.path)
                current_solution.extend(min_dist_to_entry.path)


if __name__ == "__main__":
    """If you encounter an ImportError on maze_gen when running this test
    file, run `pip install -e .` from the root of the repository. It will
    index every source file in an 'egg-info' folder and correct the path
    finding errors
    """

    from random import randint

    maze: Maze = Maze(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=False,
        gen_algorithm="Prim",
        seed=randint(0, 99999999),
        pattern=[])
    maze.generate_maze()
    print(maze)
    print(maze.config.SEED)
    solv: MazeSolver = MazeSolver(maze)
    solv.dijkstra_algorithm()
    for cell in solv.intersection_cells:
        print(
            f"Cell {cell}: Dist {solv.get_dist_from_entry(cell)} "
            "from entry, neighbours:\n",
            "\n".join(
                f"  Neighbour {neigh.coords}, At dist {neigh.distance}"
                for neigh in solv.get_neighbour_nodes(cell)), sep="")
        print()

    print("Solutions found:")
    print(*solv.shortest_paths)
