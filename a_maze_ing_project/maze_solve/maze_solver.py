
from math import inf
from a_maze_ing_project.maze_gen import (
    Maze, Directions, Movements, CellCoordinates)


class MazeSolver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

        self.shortest_path: list[CellCoordinates]
        self.solutions: list[list[CellCoordinates]]

    def dijkstra_algorithm(self) -> None:
        maze: Maze = self.maze
        intersection_cells: set[CellCoordinates] = {
            maze.config.ENTRY,
            maze.config.EXIT}
        for x in range(maze.config.WIDTH):
            for y in range(maze.config.HEIGHT):
                if len(maze.cells[x][y]) in (1, 3):
                    intersection_cells.add((x, y))
        for x, y in intersection_cells:
            maze.cells[x][y].distance_from_entry = inf
            for direction in filter(
                    lambda dir: maze.cells[x][y].walls[dir], Directions):
                pass

    def number_visited_neighbors(self, coords: CellCoordinates) -> int:
        """A function to count the number of adjacent cells for which
        `is_visited` is True. Returns this number.
        """
        visited_neighbor: int = 0
        for movement in Movements:
            neighbor = self.maze.get_neighbor_coords(
                        coords, movement.value)
            if self.maze.is_available(neighbor) is False:
                continue
            if (
                    maze.cells[neighbor[0]][neighbor[1]].is_visited is True
                    and maze.cells[coords[0]][coords[1]].walls[
                        Directions[movement.name]] is False):
                visited_neighbor += 1
        return visited_neighbor

    def update_dead_end(self) -> list[CellCoordinates]:
        """Function to update dead ends for the dead_end_filler algorithm.
        Checks all cells in the grid. If they are is_visited = False and the
        sum of (walls + adjacent cells that are is_visited = True) equals 3,
        then they are added to the list of dead ends returned.
        """
        dead_end: list[CellCoordinates] = []
        for y in range(0, (self.maze.config.HEIGHT)):
            for x in range(0, (self.maze.config.WIDTH)):
                if maze.cells[x][y].is_visited is True:
                    continue
                visited_neighbors: int = self.number_visited_neighbors((x, y))
                if (
                        maze.cells[x][y].entry is True or
                        maze.cells[x][y].exit is True):
                    continue
                if sum(self.maze.cells[x][y].walls) + visited_neighbors == 3:
                    dead_end.append((x, y))
        return dead_end

    def find_path_to_exit(self) -> None:
        """"""
        path_to_exit: list[CellCoordinates] = [maze.config.ENTRY]
        current: CellCoordinates = maze.config.ENTRY
        while current != maze.config.EXIT:
            for movement in Movements:
                neighbor = self.maze.get_neighbor_coords(
                            current, movement.value)
                if len(path_to_exit) > 1 and neighbor == path_to_exit[-2]:
                    continue
                if self.maze.is_available(neighbor) is False:
                    continue
                if (
                    self.maze.cells[
                        neighbor[0]][neighbor[1]].is_visited is False
                        and maze.cells[current[0]][current[1]].walls[
                            Directions[movement.name]] is False):
                    path_to_exit.append(neighbor)
                    current = neighbor
                    break
        self.shortest_path = path_to_exit

    def dead_end_filler(self) -> None:
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
        if maze.config.ENTRY in dead_end:
            dead_end.remove(maze.config.ENTRY)
        if maze.config.EXIT in dead_end:
            dead_end.remove(maze.config.EXIT)
        while dead_end != []:
            for cell in dead_end:
                self.maze.cells[cell[0]][cell[1]].is_visited = True
            dead_end = self.update_dead_end()
        self.find_path_to_exit()


if __name__ == "__main__":
    """If you encounter an ImportError on maze_gen when running this test
    file, run `pip install -e .` from the root of the repository. It will
    index every source file in an 'egg-info' folder and correct the path
    finding errors
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
            # [False, False, True, False, True, True, True],
            # [False, True, False, False, False, False, True],
            # [True, True, True, False, False, True, False],
            # [False, False, True, False, True, False, False],
            # [False, False, True, False, True, True, True]])
    maze.generate_maze()
    print(maze)
    solv: MazeSolver = MazeSolver(maze)
    solv.dead_end_filler()
