# from collections import deque
# # BFS Implementation
# def bfs(graph, start_node, end_node):
#     solution = []
#     frontier = deque([start_node])
#     visited = set([start_node])
#
#     while frontier:
#         selected_node = frontier.popleft()
#         solution.append(selected_node)
#
#         if selected_node == end_node:
#             return solution
#
#         for neighbor in graph.get(selected_node, []):
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 frontier.append(neighbor)
#
#     return []
#
# # DFS Implementation
# def dfs(graph, start_node, end_node):
#     solution = []
#     stack = [start_node]
#     visited = set()
#
#     while stack:
#         selected_node = stack.pop()
#         if selected_node in visited:
#             continue
#         visited.add(selected_node)
#         solution.append(selected_node)
#
#         if selected_node == end_node:
#             return solution
#
#         for neighbor in reversed(graph.get(selected_node, [])):
#             if neighbor not in visited:
#                 stack.append(neighbor)
#
#     return []
#
# # Bidirectional BFS Implementation
# def bidirectional_bfs(graph, start_node, end_node):
#     if start_node == end_node:
#         return [start_node]
#
#     front_frontier = deque([start_node])
#     back_frontier = deque([end_node])
#     front_visited = {start_node: None}
#     back_visited = {end_node: None}
#
#     while front_frontier and back_frontier:
#         # Expand front frontier
#         if front_frontier:
#             current = front_frontier.popleft()
#             for neighbor in graph.get(current, []):
#                 if neighbor not in front_visited:
#                     front_visited[neighbor] = current
#                     front_frontier.append(neighbor)
#                     if neighbor in back_visited:
#                         return construct_path(front_visited, back_visited, neighbor)
#
#         # Expand back frontier
#         if back_frontier:
#             current = back_frontier.popleft()
#             for neighbor in graph.get(current, []):
#                 if neighbor not in back_visited:
#                     back_visited[neighbor] = current
#                     back_frontier.append(neighbor)
#                     if neighbor in front_visited:
#                         return construct_path(front_visited, back_visited, neighbor)
#
#     return []
#
# # Bidirectional DFS Implementation
# def bidirectional_dfs(graph, start_node, end_node):
#     def dfs_partial(node, visited, opposite_visited, stack, path):
#         while stack:
#             current = stack.pop()
#             if current in visited:
#                 continue
#             visited[current] = path[:]
#             path.append(current)
#
#             if current in opposite_visited:
#                 return path + opposite_visited[current][::-1]
#
#             for neighbor in reversed(graph.get(current, [])):
#                 if neighbor not in visited:
#                     stack.append(neighbor)
#
#         return None
#
#     front_stack = [start_node]
#     back_stack = [end_node]
#     front_visited = {}
#     back_visited = {}
#
#     while front_stack or back_stack:
#         if front_stack:
#             front_path = dfs_partial(front_stack.pop(), front_visited, back_visited, front_stack, [])
#             if front_path:
#                 return front_path
#
#         if back_stack:
#             back_path = dfs_partial(back_stack.pop(), back_visited, front_visited, back_stack, [])
#             if back_path:
#                 return back_path
#
#     return []
#
# # Helper function to construct the path
# def construct_path(front_visited, back_visited, meeting_point):
#     path = []
#     current = meeting_point
#
#     while current:
#         path.append(current)
#         current = front_visited[current]
#     path.reverse()
#
#     current = back_visited[meeting_point]
#     while current:
#         path.append(current)
#         current = back_visited[current]
#
#     return path
#
# # Function to get user input for graph and run the algorithms
# def main():
#     graph = {}
#     print("Enter the graph (node -> neighbors). Type 'done' when finished:")
#     while True:
#         line = input()
#         if line.lower() == 'done':
#             break
#         node, *neighbors = line.split()
#         graph[node] = neighbors
#
#     start_node = input("Enter the start node: ").strip()
#     end_node = input("Enter the end node: ").strip()
#
#     print("\n--- BFS ---")
#     print("Solution:", bfs(graph, start_node, end_node))
#
#     print("\n--- DFS ---")
#     print("Solution:", dfs(graph, start_node, end_node))
#
#     print("\n--- Bidirectional BFS ---")
#     print("Solution:", bidirectional_bfs(graph, start_node, end_node))
#
#     print("\n--- Bidirectional DFS ---")
#     print("Solution:", bidirectional_dfs(graph, start_node, end_node))
#
# if __name__ == "__main__":
#     main()