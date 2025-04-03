import heapq
import time
import matplotlib.pyplot as plt
import numpy as np
class Node:
    def __init__(self, x, y, cost=0, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent
    def __lt__(self, other):
        return self.cost < other.cost
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))
def manhattan_distance(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)
def euclidean_distance(node, goal):
    return np.sqrt((node.x - goal.x)**2 + (node.y - goal.y)**2)
def astar(grid, start, goal, heuristic=manhattan_distance, allow_diagonal=False):
    open_set = []
    closed_set = set()
    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])
    heapq.heappush(open_set, (heuristic(start_node, goal_node), start_node))
    came_from = {}
    g_score = {start_node: 0}
    f_score = {start_node: heuristic(start_node, goal_node)}
    if allow_diagonal:
      moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else:
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while open_set:
        _, current_node = heapq.heappop(open_set)
        if (current_node.x, current_node.y) == (goal_node.x, goal_node.y):
            return reconstruct_path(came_from, current_node)
        closed_set.add(current_node)
        for dx, dy in moves:
            neighbor_x = current_node.x + dx
            neighbor_y = current_node.y + dy
            if (0 <= neighbor_x < len(grid) and 0 <= neighbor_y < len(grid[0]) and
                    grid[neighbor_x][neighbor_y] == 0):
                neighbor_node = Node(neighbor_x, neighbor_y)
                tentative_g_score = g_score[current_node] + 1
                if neighbor_node in g_score and tentative_g_score >= g_score[neighbor_node]:
                    continue
                g_score[neighbor_node] = tentative_g_score
                f_score[neighbor_node] = tentative_g_score + heuristic(neighbor_node, goal_node)
                if neighbor_node not in closed_set:
                    came_from[neighbor_node] = current_node
                    heapq.heappush(open_set, (f_score[neighbor_node], neighbor_node))
    return None
def bfs(grid, start, goal):
    queue = [(start[0], start[1], [])]
    visited = set()
    visited.add(start)
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while queue:
        x, y, path = queue.pop(0)
        if (x, y) == goal:
            return path + [(x, y)]
        for dx, dy in moves:
            neighbor_x = x + dx
            neighbor_y = y + dy
            if (0 <= neighbor_x < len(grid) and 0 <= neighbor_y < len(grid[0]) and
                    grid[neighbor_x][neighbor_y] == 0 and (neighbor_x, neighbor_y) not in visited):
                visited.add((neighbor_x, neighbor_y))
                queue.append((neighbor_x, neighbor_y, path + [(x, y)]))
    return None
def uniform_cost_search(grid, start, goal):
    open_set = []
    closed_set = set()
    start_node = Node(start[0], start[1], 0)
    goal_node = Node(goal[0], goal[1])
    heapq.heappush(open_set, (0, start_node))  # (cost, node)
    came_from = {}
    g_score = {start_node: 0}
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while open_set:
        cost, current_node = heapq.heappop(open_set)
        if (current_node.x, current_node.y) == (goal_node.x, goal_node.y):
            return reconstruct_path(came_from, current_node)
        closed_set.add(current_node)
        for dx, dy in moves:
            neighbor_x = current_node.x + dx
            neighbor_y = current_node.y + dy
            if (0 <= neighbor_x < len(grid) and 0 <= neighbor_y < len(grid[0]) and
                    grid[neighbor_x][neighbor_y] == 0):
                neighbor_node = Node(neighbor_x, neighbor_y)
                tentative_g_score = g_score[current_node] + 1
                if neighbor_node in g_score and tentative_g_score >= g_score[neighbor_node]:
                    continue
                g_score[neighbor_node] = tentative_g_score
                if neighbor_node not in closed_set:
                    came_from[neighbor_node] = current_node
                    heapq.heappush(open_set, (g_score[neighbor_node], neighbor_node))
    return None
def reconstruct_path(came_from, current_node):
    path = []
    while current_node:
        path.append((current_node.x, current_node.y))
        current_node = came_from.get(current_node)
    return path[::-1]
def plot_grid(grid, path=None, title="Grid"):
    plt.imshow(grid, cmap='gray', origin='upper')
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, marker='o', color='red', markersize=5, linestyle='-', linewidth=2)  # Corrected order for plotting
    plt.title(title)
    plt.show()
def main():
    grid = np.array([
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    ])
    start = (0, 0)
    goal = (9, 9)
    start_time = time.time()
    path_astar_manhattan = astar(grid, start, goal, heuristic=manhattan_distance, allow_diagonal=False)
    end_time = time.time()
    astar_manhattan_time = end_time - start_time
    if path_astar_manhattan:
        print("A* (Manhattan Distance) Path Found:", path_astar_manhattan)
        print("A* (Manhattan Distance) Time:", astar_manhattan_time)
        plot_grid(grid, path_astar_manhattan, title="A* (Manhattan Distance)")
    else:
        print("A* (Manhattan Distance) Path not found.")
    start_time = time.time()
    path_astar_euclidean = astar(grid, start, goal, heuristic=euclidean_distance, allow_diagonal=True)
    end_time = time.time()
    astar_euclidean_time = end_time - start_time
    if path_astar_euclidean:
        print("A* (Euclidean Distance) Path Found:", path_astar_euclidean)
        print("A* (Euclidean Distance) Time:", astar_euclidean_time)
        plot_grid(grid, path_astar_euclidean, title="A* (Euclidean Distance)")
    else:
        print("A* (Euclidean Distance) Path not found.")
    start_time = time.time()
    path_bfs = bfs(grid, start, goal)
    end_time = time.time()
    bfs_time = end_time - start_time
    if path_bfs:
        print("BFS Path Found:", path_bfs)
        print("BFS Time:", bfs_time)
        plot_grid(grid, path_bfs, title="BFS")
    else:
        print("BFS Path not found.")
    start_time = time.time()
    path_ucs = uniform_cost_search(grid, start, goal)
    end_time = time.time()
    ucs_time = end_time - start_time
    if path_ucs:
        print("Uniform Cost Search Path Found:", path_ucs)
        print("Uniform Cost Search Time:", ucs_time)
        plot_grid(grid, path_ucs, title="Uniform Cost Search")
    else:
        print("Uniform Cost Search Path not found.")
if __name__ == "__main__":
    main()