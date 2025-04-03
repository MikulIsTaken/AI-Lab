import numpy as np
import matplotlib.pyplot as plt
import heapq
from collections import deque

# Define movement directions for 4-way and 8-way movement
DIRECTIONS_4 = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIRECTIONS_8 = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

class Node:
    def __init__(self, position, parent=None, g=0, h=0):
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

# Heuristic functions
def heuristic(a, b, method='manhattan'):
    if method == 'manhattan':
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    elif method == 'euclidean':
        return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

# A* Algorithm
def a_star(grid, start, goal, heuristic_type='manhattan'):
    rows, cols = grid.shape
    open_list = []
    closed_set = set()
    heapq.heappush(open_list, Node(start, None, 0, heuristic(start, goal, heuristic_type)))

    while open_list:
        current = heapq.heappop(open_list)

        if current.position == goal:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        closed_set.add(current.position)
        for d in DIRECTIONS_4 if heuristic_type == 'manhattan' else DIRECTIONS_8:
            neighbor = (current.position[0] + d[0], current.position[1] + d[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[
                neighbor] == 0 and neighbor not in closed_set:
                new_g = current.g + 1
                new_h = heuristic(neighbor, goal, heuristic_type)
                heapq.heappush(open_list, Node(neighbor, current, new_g, new_h))
    return []

# BFS Algorithm
def bfs(grid, start, goal):
    queue = deque([start])
    visited = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return path[::-1]
        for d in DIRECTIONS_4:
            neighbor = (current[0] + d[0], current[1] + d[1])
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1] and grid[
                neighbor] == 0 and neighbor not in visited:
                visited[neighbor] = current
                queue.append(neighbor)
    return []

# Uniform Cost Search Algorithm
def uniform_cost_search(grid, start, goal):
    queue = [(0, start)]
    visited = {start: None}
    costs = {start: 0}
    while queue:
        cost, current = heapq.heappop(queue)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return path[::-1]
        for d in DIRECTIONS_4:
            neighbor = (current[0] + d[0], current[1] + d[1])
            new_cost = cost + 1
            if 0 <= neighbor[0] < grid.shape[0] and 0 <= neighbor[1] < grid.shape[1] and grid[
                neighbor] == 0 and (neighbor not in costs or new_cost < costs[neighbor]):
                costs[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))
                visited[neighbor] = current
    return []

# Plotting function with paths
def plot_grid(grid, path=None, title="", start=None, goal=None):
    plt.figure(figsize=(8, 8))
    plt.imshow(grid.T, cmap='gray_r', origin='lower')

    # Plot the path if it exists
    if path:
        for y, x in path:
            plt.scatter(x + 0.5, y + 0.5, color='blue', s=100)

    # Highlight start and goal points
    if start:
        plt.scatter(start[1] + 0.5, start[0] + 0.5,
                    color='green', s=200, label='Start')
    if goal:
        plt.scatter(goal[1] + 0.5, goal[0] + 0.5,
                    color='red', s=200, label='Goal')

    # Add grid lines for better visualization
    plt.xticks(np.arange(0, grid.shape[1], 1))
    plt.yticks(np.arange(0, grid.shape[0], 1))
    plt.grid(color='black', linestyle='-', linewidth=0.5)

    plt.title(title)
    plt.legend()
    plt.show()

# Create a complex grid with obstacles
grid_size = (15, 15)
grid = np.zeros(grid_size, dtype=int)
np.random.seed(42)
num_obstacles = 40
obstacles = set()
while len(obstacles) < num_obstacles:
    x, y = np.random.randint(0, grid_size[0]), np.random.randint(0, grid_size[1])
    if (x, y) not in [(0, 0), (grid_size[0]-1, grid_size[1]-1)]:
        obstacles.add((x, y))
for obs in obstacles:
    grid[obs] = 1

start, goal = (0, 0), (grid_size[0]-1, grid_size[1]-1)

# Run all algorithms
path_a_star_manhattan = a_star(grid, start, goal, 'manhattan')
path_a_star_euclidean = a_star(grid, start, goal, 'euclidean')
path_bfs = bfs(grid, start, goal)
path_ucs = uniform_cost_search(grid, start, goal)

# Plot results
plot_grid(grid, path_a_star_manhattan, "A* with Manhattan Heuristic", start=start, goal=goal)
plot_grid(grid, path_a_star_euclidean, "A* with Euclidean Heuristic", start=start, goal=goal)
plot_grid(grid, path_bfs, "Breadth-First Search", start=start, goal=goal)
plot_grid(grid, path_ucs, "Uniform Cost Search", start=start, goal=goal)
