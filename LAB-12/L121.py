from collections import deque


def bfs_unweighted(grid, start, goals, exit):
    """
    BFS for unweighted goals.
    """
    # Define possible movements
    movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Queue for BFS, contains cells in the form (x, y, path, goals_collected)
    queue = deque([(start[0], start[1], [start], set())])

    while queue:
        x, y, path, goals_collected = queue.popleft()

        # Check if we've reached the exit with all goals
        if (x, y) == exit and len(goals_collected) == len(goals):
            return path

        # Explore neighbors
        for dx, dy in movements:
            nx, ny = x + dx, y + dy

            # Check if the neighbor is within bounds and not a wall
            if (0 <= nx < len(grid)) and (0 <= ny < len(grid[0])) and grid[nx][ny] != '#':
                new_path = path + [(nx, ny)]
                new_goals_collected = goals_collected.copy()

                # Check if the neighbor is a goal
                if (nx, ny) in goals and (nx, ny) not in goals_collected:
                    new_goals_collected.add((nx, ny))

                queue.append((nx, ny, new_path, new_goals_collected))

    return None


# Example usage
grid = [
    ['.', '.', '.', '#', '.', '.', '.'],
    ['.', '#', '.', '#', '.', '#', '.'],
    ['.', '#', '.', '.', '.', '#', '.'],
    ['.', '#', '#', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.', '.', '.']
]

start = (0, 0)
goals = [(1, 1), (3, 3)]
exit = (4, 6)

path = bfs_unweighted(grid, start, goals, exit)
if path:
    print("Path found:", path)
else:
    print("No path found.")
