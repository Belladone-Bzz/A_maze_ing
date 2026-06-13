
from typing import Generator, cast
from collections import deque
from a_maze_ing_project.maze_gen import (
    Maze, Directions, Movements, CellCoordinates)


class FoundDeadEnd(Exception):
    pass


class MazeSolver:
    solving_algorithms: tuple[str, ...] = (
        "Dijkstra")

    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.ENTRY: CellCoordinates = maze.config.ENTRY
        self.EXIT: CellCoordinates = maze.config.EXIT

        self.highlighted: tuple[CellCoordinates, ...]
        self.shortest_path: deque[CellCoordinates]

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

    def record_maze_intersections(self) -> Generator[None]:
        self.intersection_cells = {
            self.ENTRY, self.EXIT}
        self.create_neighbours_list(self.ENTRY)
        self.set_distance_from_entry(self.ENTRY, (0, None))
        self.create_neighbours_list(self.EXIT)
        self.set_distance_from_entry(self.EXIT, (-1, None))
        for x in range(self.maze.config.WIDTH):
            for y in range(self.maze.config.HEIGHT):
                if sum(self.maze.cells[x][y].walls) <= 1:
                    self.intersection_cells.add((x, y))
                    self.set_distance_from_entry((x, y), (-1, None))
                    self.create_neighbours_list((x, y))
                    yield None

    def find_next_intersection(
            self, cell: CellCoordinates, dir: Directions
            ) -> Node:
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

    def set_nodes_distance_from_entry(self) -> Generator[None]:
        current_nodes: list[CellCoordinates] = [self.ENTRY]
        temp_neighbours: list[CellCoordinates] = []
        processed_nodes: set[CellCoordinates] = set()
        distance_from_entry: float
        entry_to_next_node: float
        while len(processed_nodes) < len(self.intersection_cells):
            for known_node in current_nodes:
                for next_node in self.get_neighbour_nodes(known_node):
                    entry_to_next_node = (
                        self.get_dist_from_entry(known_node)[0]
                        + next_node.distance)
                    distance_from_entry = self.get_dist_from_entry(
                        next_node.coords)[0]
                    if (distance_from_entry == -1
                            or distance_from_entry > entry_to_next_node):
                        self.highlighted = next_node.path
                        self.set_distance_from_entry(
                            next_node.coords, (
                                entry_to_next_node,
                                tuple([known_node, *next_node.path][-2::-1])))
                        yield None
                    temp_neighbours.append(next_node.coords)
            processed_nodes.update(current_nodes)
            current_nodes = temp_neighbours
            temp_neighbours = []

    def get_neighbour_nodes(
            self, cell: CellCoordinates) -> list[Node]:
        return cast(list[MazeSolver.Node], getattr(
            self.maze.cells[cell[0]][cell[1]], "neighbour_nodes"))

    def create_neighbours_list(self, cell: CellCoordinates) -> None:
        setattr(
            self.maze.cells[cell[0]][cell[1]], "neighbour_nodes", [])

    def get_dist_from_entry(
            self, cell: CellCoordinates
            ) -> tuple[int, tuple[CellCoordinates, ...]]:
        return cast(tuple[int, tuple[CellCoordinates, ...]], getattr(
            self.maze.cells[cell[0]][cell[1]], "distance_from_entry"))

    def set_distance_from_entry(
            self, cell: CellCoordinates,
            distance: tuple[int, tuple[CellCoordinates, ...] | None]) -> None:
        setattr(
            self.maze.cells[cell[0]][cell[1]], "distance_from_entry", distance)

    # _________________________________________________________________________
    #                              ALGORITHMS
    # _________________________________________________________________________

    def dijkstra_algorithm(self) -> Generator[None]:
        for _ in self.generate_cell_graph():
            yield None
        for _ in self.set_nodes_distance_from_entry():
            yield None
        self.highlighted = tuple()
        self.shortest_path = deque([self.maze.config.EXIT])
        while self.ENTRY != self.shortest_path[0]:
            self.shortest_path.extendleft(self.get_dist_from_entry(
                self.shortest_path[0])[1])
            yield None

    def dead_end_filler(self) -> None:
        """"""


    def solve_maze(self, algorithm: str) -> None:
        pass


if __name__ == "__main__":
    """If you encounter an ImportError on maze_gen when running this test
    file, run `pip install -e .` from the root of the repository. It will
    index every source file in an 'egg-info' folder and correct the path
    finding errors
    """

    from random import randint
    from sys import argv

    maze: Maze = Maze(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=False,
        gen_algorithm="Prim",
        seed=randint(0, 99999999),
        pattern=[])
    maze.generate_maze()
    print(maze)
    print(maze.config.SEED)
    solv: MazeSolver = MazeSolver(maze)

    if len(argv) < 2 or argv[1] == "dijkstra":
        for _ in solv.dijkstra_algorithm():
            pass
        # for cell in solv.intersection_cells:
        #     print(
        #         f"Cell {cell}: Dist {solv.get_dist_from_entry(cell)} "
        #         "from entry, neighbours:\n",
        #         "\n".join(
        #             f"  Neighbour {neigh.coords}, At dist {neigh.distance}"
        #             for neigh in solv.get_neighbour_nodes(cell)), sep="")
        #     print()

    print("Solutions found:")
    print(solv.shortest_path)
