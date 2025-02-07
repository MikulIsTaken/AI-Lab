from collections import deque
def bfs(maze, start, end):
    queue = deque([(start, [start])])
    visited = set()
    nodes_explored = 0
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path, nodes_explored
        if (x, y) in visited:
            continue
        visited.add((x, y))
        nodes_explored += 1
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 1:
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None, nodes_explored
def dfs(maze, start, end):
    stack = [(start, [start])]
    visited = set()
    nodes_explored = 0
    while stack:
        (x, y), path = stack.pop()
        if (x, y) == end:
            return path, nodes_explored
        if (x, y) in visited:
            continue
        visited.add((x, y))
        nodes_explored += 1
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 1:
                stack.append(((nx, ny), path + [(nx, ny)]))
    return None, nodes_explored
def iddfs(maze, start, end, max_depth):
    def dls(node, depth, path):
        if depth == 0:
            return None
        if node == end:
            return path
        x, y = node
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 1
                    and (nx, ny) not in path):
                result = dls((nx, ny), depth - 1, path + [(nx, ny)])
                if result:
                    return result
        return None
    for depth in range(1, max_depth + 1):
        result = dls(start, depth, [start])
        if result:
            return result, depth
    return None, max_depth
maze = [
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 0, 1, 1],
    [1, 1, 1, 1, 0],
    [1, 0, 0, 1, 1]
]
start = (0, 0)
end = (4, 4)
bfs_path, bfs_nodes = bfs(maze, start, end)
dfs_path, dfs_nodes = dfs(maze, start, end)
iddfs_path, iddfs_nodes = iddfs(maze, start, end, 20)
print("BFS Path:", bfs_path, "Nodes explored:", bfs_nodes)
print("DFS Path:", dfs_path, "Nodes explored:", dfs_nodes)
print("IDDFS Path:", iddfs_path, "Nodes explored:", iddfs_nodes)
if bfs_nodes <= dfs_nodes and bfs_nodes <= iddfs_nodes:
    print("BFS is the best in terms of explored nodes for shortest path.")
elif dfs_nodes <= bfs_nodes and dfs_nodes <= iddfs_nodes:
    print("DFS is better in terms of node exploration but may not give the shortest path.")
else:
    print("IDDFS is useful for depth-limited exploration but may not always be optimal.")


