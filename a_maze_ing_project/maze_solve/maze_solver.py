
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

    def dead_end_filler(self) -> None:
        """"""
        if Maze.Config.PERFECT is False:
            print("Dead end filler algorithm can only be used for perfect" \
                  "mazes.")


if __name__ == "__main__":
    """If you encounter an ImportError on maze_gen when running this test
    file, run `pip install -e .` from the root of the repository. It will
    index every source file in an 'egg-info' folder and correct the path
    finding errors
    """

    from random import randint

    maze: Maze = Maze(
        width=25,
        height=25,
        entry=(0, 0),
        exit=(0, 1),
        perfect=False,
        gen_algorithm="Prim",
        seed=randint(0, 99999999),
        pattern=[
            [False, False, True, False, True, True, True],
            [False, True, False, False, False, False, True],
            [True, True, True, False, False, True, False],
            [False, False, True, False, True, False, False],
            [False, False, True, False, True, True, True]])
    maze.generate_maze()
    print(maze)
    solv: MazeSolver = MazeSolver(maze)
    solv.dijkstra_algorithm()
