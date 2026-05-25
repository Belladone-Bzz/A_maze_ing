### Depth-First Search Algorithm
Depth-First Search is a fundamental algorithm used for traversing or searching tree or graph data structures. Starting at the root node, DFS explores as far as possible along each branch before backtracking. This approach mimics how we naturally would solve mazes.

**Advantages:**
- Memory efficient: Stores only a stack of nodes.
- Ideal for deep but narrow trees or graphs.
- Easy to implement using recursion.

**Disadvantages:**
- Can get stuck in cycles without cycle detection.
- Doesn’t guarantee the shortest path in unweighted graphs.

**Seems ideal for perfect maze solving.**
### Breadth-First Search Algorithm
Starting at the root node, BFS visits all its neighbors first, then their neighbors, and so on. This approach guarantees that the **shortest path** is found in unweighted graphs, making it ideal for scenarios where finding the shortest route is crucial.

**Advantages:**
- Guarantees the shortest path in unweighted graphs.

**Disadvantages:**
- Memory-intensive: Stores all nodes at the current level.
- Can be problematic for very wide trees or graphs.

**Seems ideal for non-perfect maze solving.**
### Dead-End Filling Algorithm
Dead-End Filling is exactly what it sounds like: an algorithm that systematically fills in all dead ends to get the final path in the end. A dead end is identified as any cell that has 3 walls surrounding it. By filling these dead ends, you can simplify the maze and focus on the potential paths that lead to the solution.

The algorithm goes through each cell in the maze iteratively, filling in the dead ends from the top down. Then it repeats the same thing until we get the final path. This method is particularly interesting because it transforms a complex network of pathways into a single path in the case of a perfect maze.

**Advantages:**
- Dead-end filling efficiently reduces a maze by systematically eliminating dead ends. It ensures a clear solution path without the need for backtracking.

**Disadvantages:**
- While highly effective for perfect mazes, this algorithm may not be as effective for mazes with multiple solutions or loops.

**Seems ideal for perfect maze solving.**
### Dijkstra Algorithm
This is a non-heuristic algorithm that guarantees the shortest path by exploring all possible routes from the starting point to the destination. It does so by systematically considering the shortest distance to each node and updating paths until the most efficient route is found.

Dijkstra's algorithm finds the shortest path from one vertex to all other vertices. It does so by repeatedly selecting the nearest un-visited vertex and calculating the distance to all the un-visited neighboring vertices. To find the shortest path, Dijkstra's algorithm needs to know which vertex is the source, it needs a way to mark vertices as visited, and it needs an overview of the current shortest distance to each vertex as it works its way through the graph, updating these distances when a shorter distance is found.

**Seems ideal for perfect maze solving.**
### A* Algorithm
The A* algorithm is a powerful and widely used graph traversal and path finding algorithm. It finds the shortest path between a starting node and a goal node in a weighted graph.
The A* algorithm combines the best aspects of two other algorithms:

1. Dijkstra's Algorithm: This algorithm finds the shortest path to all nodes from a single source node.
2. Greedy Best-First Search: This algorithm explores the node that appears to be closest to the goal, based on a heuristic function.

**Seems the most efficient for maze solving.**