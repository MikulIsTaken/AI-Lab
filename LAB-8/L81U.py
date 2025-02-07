import heapq  # For priority queue operations in uniform cost search
from collections import deque  # For queue operations in BFS
import networkx as nx  # For creating and manipulating graphs
import matplotlib.pyplot as plt  # For visualization

# Visualization Function
def visualize_graph(graph, path, title):
    """
    Parameters:
    - graph: Dictionary representing the graph structure
    - path: List of nodes representing the found path
    - title: String for the visualization title
    """

    # Create a directed graph object
    G = nx.DiGraph()  # DiGraph means edges have direction (arrows)

    # Iterate through each node in the graph
    for node in graph:
        G.add_node(node)  # Add the current node to the graph
        # For each neighbor and its edge weight connected to current node
        for neighbor, weight in graph[node]:
            # Add a directed edge from node to neighbor with given weight
            G.add_edge(node, neighbor, weight=weight)

    # Create a layout for the nodes
    # spring_layout arranges nodes using force-directed algorithm
    # seed=42 ensures consistent layout each time
    pos = nx.spring_layout(G, seed=42)

    # Initialize lists to store colors for nodes and edges
    node_colors = []
    edge_colors = []
    path_edges = []

    # If a path was found
    if path:
        # Create pairs of consecutive nodes in the path
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

        # Color edges: red if in path, gray if not
        for edge in G.edges():
            if edge in path_edges or (edge[1], edge[0]) in path_edges:
                edge_colors.append('red')
            else:
                edge_colors.append('gray')

        # Color nodes: red if in path, lightblue if not
        for node in G.nodes():
            if node in path:
                node_colors.append('red')
            else:
                node_colors.append('lightblue')
    else:
        # If no path, color everything default colors
        node_colors = 'lightblue'
        edge_colors = 'gray'

    # Create the visualization
    plt.figure(figsize=(10, 6))  # Set figure size

    # Draw the graph with specified properties
    nx.draw(G, pos,
            with_labels=True,  # Show node labels
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=800,
            font_size=12,
            arrows=True)  # Show direction of edges

    # Add weight labels to edges
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Set title and save/show the plot
    plt.title(title)
    plt.savefig(f"{title.replace(' ', '_')}.png")
    plt.show()


# Uniform Cost Search Implementation
def uniform_cost_search(graph, start, goal):
    """
    Parameters:
    - graph: Dictionary representing the graph structure
    - start: Starting node
    - goal: Target node
    Returns:
    - path: List of nodes in the shortest path
    - cost: Total cost of the path
    """

    # Initialize priority queue with starting node
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, node)

    # Track costs and parents for path reconstruction
    cost_so_far = {start: 0}  # Track minimum cost to reach each node
    parent = {start: None}  # Track path

    while priority_queue:
        # Get node with lowest cost from queue
        current_cost, current_node = heapq.heappop(priority_queue)

        # If we reached the goal, we're done
        if current_node == goal:
            break

        # Skip if we've found a better path
        if current_cost > cost_so_far[current_node]:
            continue

        # Explore neighbors
        for neighbor, edge_cost in graph.get(current_node, []):
            new_cost = current_cost + edge_cost

            # If we found a better path to neighbor
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current_node
                heapq.heappush(priority_queue, (new_cost, neighbor))

    # Reconstruct path
    path = []
    node = goal

    # If goal not reached, return None
    if node not in parent:
        return None, None

    # Build path by following parent pointers
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, cost_so_far.get(goal, None)


# Breadth-First Search Implementation
def bfs(graph, start, goal):
    """
    Parameters:
    - graph: Dictionary representing the graph structure
    - start: Starting node
    - goal: Target node
    Returns:
    - path: List of nodes in the shortest path
    - cost: Number of edges in path
    """

    # Initialize queue with start node
    queue = deque([start])
    parent = {start: None}  # Track path
    visited = set([start])  # Track visited nodes

    while queue:
        current_node = queue.popleft()  # Get next node to explore

        if current_node == goal:
            break

        # Explore unvisited neighbors
        for neighbor, _ in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current_node
                queue.append(neighbor)

    # Reconstruct path
    path = []
    node = goal

    # If goal not reached, return None
    if node not in parent:
        return None, None

    # Build path by following parent pointers
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    # In BFS, cost is just number of edges
    cost = len(path) - 1

    return path, cost

def visualize_path(path, cost):
    """Simple helper function to print path and cost"""
    if path is None:
        print("No path found.")
    else:
        print("Path found:", ' -> '.join(path))
        print("Total cost:", cost)

# Test graphs
graph_weighted = {
    'A': [('B', 2), ('C', 4)],  # Node A connects to B (cost 2) and C (cost 4)
    'B': [('D', 5), ('E', 3)],  # Node B connects to D (cost 5) and E (cost 3)
    'C': [('F', 6)],            # Node C connects to F (cost 6)
    'D': [('G', 1)],            # Node D connects to G (cost 1)
    'E': [('G', 7)],            # Node E connects to G (cost 7)
    'F': [('G', 4)],            # Node F connects to G (cost 4)
    'G': []                     # Node G has no outgoing edges
}

# Same graph structure but all edges have cost 1
graph_unweighted = {
    'A': [('B', 1), ('C', 1)],
    'B': [('D', 1), ('E', 1)],
    'C': [('F', 1)],
    'D': [('G', 1)],
    'E': [('G', 1)],
    'F': [('G', 1)],
    'G': []
}