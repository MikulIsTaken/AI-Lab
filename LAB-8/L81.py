import heapq
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
def visualize_graph(graph, path, title):
    G = nx.DiGraph()
    for node in graph:
        G.add_node(node)
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)
    pos = nx.spring_layout(G, seed=42)
    node_colors = []
    edge_colors = []
    path_edges = []
    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        for edge in G.edges():
            if edge in path_edges or (edge[1], edge[0]) in path_edges:
                edge_colors.append('red')
            else:
                edge_colors.append('gray')
        for node in G.nodes():
            if node in path:
                node_colors.append('red')
            else:
                node_colors.append('lightblue')
    else:
        node_colors = 'lightblue'
        edge_colors = 'gray'
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
            node_size=800, font_size=12, arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title(title)
    plt.savefig(f"{title.replace(' ', '_')}.png")
    plt.show()
def uniform_cost_search(graph, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    cost_so_far = {start: 0}
    parent = {start: None}
    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        if current_node == goal:
            break
        if current_cost > cost_so_far[current_node]:
            continue
        for neighbor, edge_cost in graph.get(current_node, []):
            new_cost = current_cost + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current_node
                heapq.heappush(priority_queue, (new_cost, neighbor))
    path = []
    node = goal
    if node not in parent:
        return None, None
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path, cost_so_far.get(goal, None)
def bfs(graph, start, goal):
    queue = deque([start])
    parent = {start: None}
    visited = set([start])
    while queue:
        current_node = queue.popleft()
        if current_node == goal:
            break
        for neighbor, _ in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)
    path = []
    node = goal
    if node not in parent:
        return None, None
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    cost = len(path) - 1
    return path, cost
def visualize_path(path, cost):
    if path is None:
        print("No path found.")
    else:
        print("Path found:", ' -> '.join(path))
        print("Total cost:", cost)
graph_weighted = {
    'A': [('B', 2), ('C', 4)],
    'B': [('D', 5), ('E', 3)],
    'C': [('F', 6)],
    'D': [('G', 1)],
    'E': [('G', 7)],
    'F': [('G', 4)],
    'G': []
}
start = 'A'
goal = 'G'
graph_unweighted = {
    'A': [('B', 1), ('C', 1)],
    'B': [('D', 1), ('E', 1)],
    'C': [('F', 1)],
    'D': [('G', 1)],
    'E': [('G', 1)],
    'F': [('G', 1)],
    'G': []
}
print("Uniform Cost Search on Weighted Graph:")
path_ucs_weighted, cost_ucs_weighted = uniform_cost_search(graph_weighted, start, goal)
visualize_path(path_ucs_weighted, cost_ucs_weighted)
visualize_graph(graph_weighted, path_ucs_weighted, "UCS on Weighted Graph")
print("\nUniform Cost Search on Unweighted Graph (all weights=1):")
path_ucs_unweighted, cost_ucs_unweighted = uniform_cost_search(graph_unweighted, start, goal)
visualize_path(path_ucs_unweighted, cost_ucs_unweighted)
visualize_graph(graph_unweighted, path_ucs_unweighted, "UCS on Unweighted Graph")
print("\nBFS on Unweighted Graph (all weights=1):")
path_bfs_unweighted, cost_bfs_unweighted = bfs(graph_unweighted, start, goal)
visualize_path(path_bfs_unweighted, cost_bfs_unweighted)
visualize_graph(graph_unweighted, path_bfs_unweighted, "BFS on Unweighted Graph")