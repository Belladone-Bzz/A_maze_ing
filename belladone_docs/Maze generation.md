Maze generation algorithms are not here to play, they have applications in areas ranging from robotics to even art. Understanding how they work can give you insights into broader concepts in computer science, such as graph theory and path-finding.
Many maze generation algorithms exist, some of them are described bellow.

### Kruskal’s Algorithm:
Kruskal’s algorithm does not start at a root node and try to find paths like other algorithms. This algorithm works by removing the walls between cells randomly and carving path, making a perfect maze.

**Method:**
- Initialisation:
	- Start with a list of all walls
	- Create a set for each cell, initially containing just that cell

- Wall Removal Process:
	For each wall, if the cells divided by the wall belong to different sets:
	- Remove wall
	- Merge the sets of previously divided cells

To make this algorithm efficient, we use a **disjoint-set** data structure. This structure ensures that union and find operations are almost instantaneous, keeping the algorithm running smoothly.

Create **perfect maze**

### Wilson’s Algorithm:
Wilson’s Algorithm is a random walk-based model. It starts with an initial cell and performs a loop-erased random walk to carve out a maze. This algorithm ensures uniform spanning trees, making it both fascinating and a bit unpredictable.

**Method:**
- **Start with an arbitrary cell:** Choose any cell in the grid to declare as the beginning to the maze.
- **Random walk initiation:** Pick another random cell and start a random walk until you hit a cell that’s already part of the maze.
- **Loop erasing:** If the walk forms a loop, erase it before proceeding.
- **Path addition:** Once the walk connects to the maze, add the path.
- **Repeat:** Continue this process with new starting cells until the entire grid is filled.

This method might sound complex, but it ensures that the maze is created without any biases. Each run of the algorithm results in a completely different maze.

Create **perfect maze**

### Iterative backtracking Algorithm:
The beauty of Iterative Backtracking lies in its clever adaptation of DFS for maze generation. Instead of using walls to determine dead-ends, we use visited cells.

**Method:**
 - **Initialise the Grid:**
	- Start with a grid full of walls.
	- Choose a random cell as the starting point and mark it as part of the maze.
- **Use a stack to keep track of the path:**
	- Push the starting cell onto the stack.
	- While the stack is not empty:
		- Pop a cell from the stack and mark it as part of the maze.
		- Push its unvisited neighbours onto the stack, removing the walls between the current cell and the neighbour.
		- If there are no unvisited neighbours, backtrack to the previous cell by popping the stack until an unvisited neighbour is found.

Another maze-making algorithm such as Wilson’s Algorithm would, on average make a maze that goes diagonally downwards from start to end. However, iterative backtracking makes a random maze with lots of turns and twists.

The depth-first nature of this algorithm is why this happens. It explores each path deeply before backtracking, leading to long, winding corridors that twist and turn as they reach dead-ends and backtrack.

As the algorithm backtracks from dead-ends, it creates a dense network of paths that intersect and loop around, making the maze complex and full of twists.

Create **perfect maze**

### **Hunt-and-Kill Algorithm:

**Method:**
- Choose a starting location.
- Perform a random walk, carving passages to unvisited neighbors, until the current cell has no unvisited neighbors.
- Enter “hunt” mode, where you scan the grid looking for an unvisited cell that is adjacent to a visited cell. If found, carve a passage between the two and let the formerly unvisited cell be the new starting location.
- Repeat steps 2 and 3 until the hunt mode scans the entire grid and finds no unvisited cells.

https://weblog.jamisbuck.org/2011/1/24/maze-generation-hunt-and-kill-algorithm
Create **perfect maze**

### Randomized Prim's Algorithm:
Rather than working edgewise across the entire graph, it starts at one point, and grows outward from that point.

**Method:**
- Choose an arbitrary vertex from G (the graph), and add it to some (initially empty) set V.
- Choose the edge with the smallest weight from G, that connects a vertex in V with another vertex _not_ in V.
- Add that edge to the minimal spanning tree, and the edge’s other vertex to V.
- Repeat steps 2 and 3 until V includes every vertex in G.

With one little change, it becomes a suitable method for generating mazes: just change step 2 so that instead of selecting the edge with the smallest weight, you select an edge at random, as long as it bridges the so-called “frontier” of the maze (the set of edges that move from within the maze, to a cell that is outside the maze).

https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
Create **perfect maze**

