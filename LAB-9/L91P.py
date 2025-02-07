import heapq

# Puzzle state definition with a custom comparator
class PuzzleState:
    def __init__(self, board, zero_pos, moves=0, parent=None):
        self.board = board                # 3x3 board configuration
        self.zero_pos = zero_pos          # (row, col) of the blank (0)
        self.moves = moves                # Number of moves made so far
        self.parent = parent              # Pointer to the parent PuzzleState

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(map(tuple, self.board)))

    def __lt__(self, other):
        # Required for heapq comparisons when priorities are equal
        return self.moves < other.moves

    def get_neighbors(self):
        neighbors = []
        x, y = self.zero_pos
        # Directions: down, up, right, left
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = [row[:] for row in self.board]  # Deep copy the board
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                neighbors.append(PuzzleState(new_board, (new_x, new_y), self.moves + 1, self))
        return neighbors

# Heuristic H1: Count of misplaced tiles (ignoring the blank)
def h1_misplaced_tiles(state):
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    count = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != goal_state[i][j] and state.board[i][j] != 0:
                count += 1
    return count

# Heuristic H2: Sum of Manhattan distances for each tile from its goal position
def h2_manhattan_distance(state):
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1)
    }
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = state.board[i][j]
            if tile != 0:
                goal_x, goal_y = goal_positions[tile]
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

# A* search with heuristic H1 (misplaced tiles)
def a_star_h1(start_state):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (h1_misplaced_tiles(start_state), start_state))

    while open_set:
        _, current_state = heapq.heappop(open_set)
        if current_state.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            return current_state
        closed_set.add(current_state)
        for neighbor in current_state.get_neighbors():
            if neighbor not in closed_set:
                cost = neighbor.moves + h1_misplaced_tiles(neighbor)
                heapq.heappush(open_set, (cost, neighbor))
    return None

# A* search with heuristic H2 (Manhattan distance)
def a_star_h2(start_state):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (h2_manhattan_distance(start_state), start_state))

    while open_set:
        _, current_state = heapq.heappop(open_set)
        if current_state.board == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            return current_state
        closed_set.add(current_state)
        for neighbor in current_state.get_neighbors():
            if neighbor not in closed_set:
                cost = neighbor.moves + h2_manhattan_distance(neighbor)
                heapq.heappush(open_set, (cost, neighbor))
    return None

# Function to compare the two heuristic approaches
def compare_heuristics(start_state):
    # Solve using H1
    h1_solution = a_star_h1(start_state)
    h1_depth = h1_solution.moves
    h1_nodes_explored = 0
    current = h1_solution
    while current:
        h1_nodes_explored += 1
        current = current.parent

    # Solve using H2
    h2_solution = a_star_h2(start_state)
    h2_depth = h2_solution.moves
    h2_nodes_explored = 0
    current = h2_solution
    while current:
        h2_nodes_explored += 1
        current = current.parent

    return {
        'H1_nodes_explored': h1_nodes_explored,
        'H1_depth': h1_depth,
        'H2_nodes_explored': h2_nodes_explored,
        'H2_depth': h2_depth
    }

# Testing the solution with a sample start state
if __name__ == '__main__':
    # Example start state: the blank (0) is at position (1,1)
    start_state = PuzzleState([[1, 2, 3],
                               [4, 0, 5],
                               [7, 8, 6]], (1, 1))
    performance = compare_heuristics(start_state)
    print(performance)
