def bfs(graph, start_node, end_node):
    solution = []
    costs = 0
    frontier = []
    visited = []
    frontier.append(start_node)
    visited.append(start_node)
    while frontier:
        selected_node = frontier.pop(0)
        if selected_node == end_node:
            solution.append(selected_node)
            break
        solution.append(selected_node)
        for neighbour in graph[selected_node]:
            if neighbour not in visited:
                frontier.append(neighbour)
                visited.append(neighbour)
        costs += 1
    return solution, costs
print("Enter the graph (node -> neighbors). Type 'done' when finished:")
state_space = {}
while True:
    line = input()
    if line.lower() == "done":
        break
    parts = line.split()
    node = parts[0]
    neighbors = parts[1:] if len(parts) > 1 else []
    state_space[node] = neighbors
start_state = input("Enter the start node: ")
goal_state = input("Enter the end node: ")
solution, costs = bfs(state_space, start_state, goal_state)
print("Solution: {}".format(solution))
print("Costs: {}".format(costs))