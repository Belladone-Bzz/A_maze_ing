### Depth-First Search
Depth-First Search is a fundamental algorithm used for traversing or searching tree or graph data structures. Starting at the root node, DFS explores as far as possible along each branch before backtracking. This approach mimics how we naturally would solve mazes.

**Advantages:**
- Memory efficient: Stores only a stack of nodes.
- Ideal for deep but narrow trees or graphs.
- Easy to implement using recursion.

**Disadvantages:**
- Can get stuck in cycles without cycle detection.
- Doesn’t guarantee the shortest path in unweighted graphs.

**Seems ideal for perfect maze solving.**
### Breadth-First Search
Starting at the root node, BFS visits all its neighbors first, then their neighbors, and so on. This approach guarantees that the **shortest path** is found in unweighted graphs, making it ideal for scenarios where finding the shortest route is crucial.

**Advantages:**
- Guarantees the shortest path in unweighted graphs.

**Disadvantages:**
- Memory-intensive: Stores all nodes at the current level.
- Can be problematic for very wide trees or graphs.

**Seems ideal for non-perfect maze solving.**

### Dead-End Filling
Dead-End Filling is exactly what it sounds like: an algorithm that systematically fills in all dead ends to get the final path in the end. A dead end is identified as any cell that has 3 walls surrounding it. By filling these dead ends, you can simplify the maze and focus on the potential paths that lead to the solution.