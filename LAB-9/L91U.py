import heapq
from typing import List, Tuple, Optional, Callable, Set

# Define the type for a state: a tuple of 9 integers.
State = Tuple[int, ...]


def print_state(state: State) -> None:
    """Print a state in 3x3 format."""
    for i in range(0, 9, 3):
        print(state[i:i + 3])
    print()


def get_neighbors(state: State) -> List[Tuple[State, str]]:
    """Generate all possible moves (neighbors) from a given state.

    Returns a list of tuples (neighbor_state, move) where 'move' is a string indicating
    the direction in which the blank (0) moves.
    """
    neighbors = []
    side = 3  # 3x3 board
    blank_index = state.index(0)
    row, col = divmod(blank_index, side)

    moves = []
    if row > 0:
        moves.append((-1, 0, "Up"))
    if row < side - 1:
        moves.append((1, 0, "Down"))
    if col > 0:
        moves.append((0, -1, "Left"))
    if col < side - 1:
        moves.append((0, 1, "Right"))

    for dr, dc, move in moves:
        new_row, new_col = row + dr, col + dc
        new_index = new_row * side + new_col
        new_state = list(state)
        # Swap blank with the adjacent tile
        new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
        neighbors.append((tuple(new_state), move))

    return neighbors


def heuristic_misplaced(state: State, goal: State) -> int:
    """Heuristic H1: Count the number of misplaced tiles (ignoring the blank)."""
    return sum(1 for i, tile in enumerate(state) if tile != 0 and tile != goal[i])


def heuristic_manhattan(state: State, goal: State) -> int:
    """Heuristic H2: Sum of Manhattan distances of all tiles from their goal positions."""
    distance = 0
    side = 3
    for index, tile in enumerate(state):
        if tile != 0:
            current_row, current_col = divmod(index, side)
            goal_index = goal.index(tile)
            goal_row, goal_col = divmod(goal_index, side)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance


class Node:
    def __init__(self, state: State, parent: Optional['Node'] = None,
                 move: Optional[str] = None, g: int = 0, h: int = 0):
        self.state = state
        self.parent = parent
        self.move = move  # Move taken to reach this state from the parent
        self.g = g  # Cost so far (number of moves)
        self.h = h  # Heuristic estimate to goal
        self.f = g + h  # Total estimated cost

    def __lt__(self, other: 'Node'):
        return self.f < other.f


def reconstruct_path(node: Node) -> List[str]:
    """Reconstruct the path from the start node to the current node."""
    path = []
    current = node
    while current.parent is not None:
        path.append(current.move)
        current = current.parent
    path.reverse()
    return path


def a_star(initial: State, goal: State, heuristic_func: Callable[[State, State], int]) -> Tuple[
    Optional[List[str]], int, int]:
    """
    Perform A* search.

    Returns:
      - A list of moves leading from the initial state to the goal state (if found),
      - The total number of nodes expanded,
      - The solution depth (number of moves).
    """
    open_list = []
    closed_set: Set[State] = set()

    h_initial = heuristic_func(initial, goal)
    start_node = Node(state=initial, parent=None, move=None, g=0, h=h_initial)
    heapq.heappush(open_list, start_node)

    nodes_expanded = 0

    while open_list:
        current_node = heapq.heappop(open_list)

        # Goal check
        if current_node.state == goal:
            path = reconstruct_path(current_node)
            return path, nodes_expanded, current_node.g

        closed_set.add(current_node.state)
        nodes_expanded += 1

        for neighbor_state, move in get_neighbors(current_node.state):
            if neighbor_state in closed_set:
                continue
            g = current_node.g + 1
            h = heuristic_func(neighbor_state, goal)
            neighbor_node = Node(state=neighbor_state, parent=current_node, move=move, g=g, h=h)

            # Add to open list; duplicate states in the open list are acceptable for simplicity
            heapq.heappush(open_list, neighbor_node)

    # No solution found
    return None, nodes_expanded, -1


def main():
    # Example initial state (0 represents the blank)
    initial_state: State = (1, 2, 3,
                            4, 0, 6,
                            7, 5, 8)

    # Define the goal state
    goal_state: State = (1, 2, 3,
                         4, 5, 6,
                         7, 8, 0)

    print("Initial State:")
    print_state(initial_state)
    print("Goal State:")
    print_state(goal_state)

    # Solve using H1: Misplaced Tiles
    print("Solving using Heuristic H1 (Misplaced Tiles)...")
    path1, nodes_expanded1, depth1 = a_star(initial_state, goal_state, heuristic_misplaced)
    if path1 is not None:
        print("Solution found!")
        print("Moves:", path1)
        print("Solution depth:", depth1)
        print("Nodes expanded:", nodes_expanded1)
    else:
        print("No solution found using H1.")

    print("\n--------------------------------------\n")

    # Solve using H2: Manhattan Distance
    print("Solving using Heuristic H2 (Manhattan Distance)...")
    path2, nodes_expanded2, depth2 = a_star(initial_state, goal_state, heuristic_manhattan)
    if path2 is not None:
        print("Solution found!")
        print("Moves:", path2)
        print("Solution depth:", depth2)
        print("Nodes expanded:", nodes_expanded2)
    else:
        print("No solution found using H2.")


if __name__ == "__main__":
    main()
