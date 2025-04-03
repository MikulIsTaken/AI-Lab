import heapq
from collections import deque
import time
import math
from typing import List, Tuple, Optional, Set, Dict, FrozenSet, NamedTuple
class Point(NamedTuple):
    row: int
    col: int
class SearchNode:
    def __init__(self, position: Point, collected_goals: FrozenSet[Point], cost: float, parent: Optional['SearchNode'], action: Optional[str] = None):
        self.position = position
        self.collected_goals = collected_goals
        self.cost = cost
        self.parent = parent
        self.action = action
    def __lt__(self, other: 'SearchNode') -> bool:
        if self.cost != other.cost:
            return self.cost < other.cost
        return self.position < other.position
    def __hash__(self) -> int:
        return hash((self.position, self.collected_goals))
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SearchNode):
            return NotImplemented
        return self.position == other.position and self.collected_goals == other.collected_goals
    def get_state_tuple(self) -> Tuple[Point, FrozenSet[Point]]:
        return (self.position, self.collected_goals)
class Grid:
    def __init__(self, grid_layout: List[str]):
        self.layout = [list(row) for row in grid_layout]
        self.rows = len(grid_layout)
        self.cols = len(grid_layout[0]) if self.rows > 0 else 0
        self.start_pos: Optional[Point] = None
        self.exit_pos: Optional[Point] = None
        self.goal_positions: Set[Point] = set()
        self.goal_priorities: Dict[Point, int] = {}
        goal_counter = 1
        for r in range(self.rows):
            for c in range(self.cols):
                char = self.layout[r][c]
                pos = Point(r, c)
                if char == 'S':
                    self.start_pos = pos
                elif char == 'E':
                    self.exit_pos = pos
                elif char.isdigit():
                    goal_pos = pos
                    self.goal_positions.add(goal_pos)
                    self.goal_priorities[goal_pos] = int(char)
                elif char == 'G':
                    goal_pos = pos
                    self.goal_positions.add(goal_pos)
                    self.goal_priorities[goal_pos] = 1
                    self.layout[r][c] = 'G'
        if not self.start_pos:
            raise ValueError("Start position 'S' not found in grid.")
        if not self.exit_pos:
            raise ValueError("Exit position 'E' not found in grid.")
        if not self.goal_positions:
            print("Warning: No goal positions ('G' or '1'-'9') found in grid.")
        self.all_goals_fs = frozenset(self.goal_positions)
    def is_wall(self, pos: Point) -> bool:
        return self.layout[pos.row][pos.col] == '#'
    def is_valid(self, pos: Point) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols and not self.is_wall(pos)
    def get_neighbors(self, pos: Point) -> List[Tuple[Point, str]]:
        neighbors = []
        moves = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        for action, (dr, dc) in moves.items():
            new_row, new_col = pos.row + dr, pos.col + dc
            new_pos = Point(new_row, new_col)
            if self.is_valid(new_pos):
                neighbors.append((new_pos, action))
        return neighbors
    def print_path(self, path: Optional[List[Point]]):
        if not path:
            print("No path found.")
            return
        temp_grid = [row[:] for row in self.layout]
        path_markers = {}
        collected_on_path = set()
        path_goals_order = []
        for i, pos in enumerate(path):
             if i == 0:
                 marker = 'S'
             elif pos == self.exit_pos and i == len(path) - 1:
                 marker = 'E'
             elif pos in self.goal_positions and pos not in collected_on_path:
                 marker = self.layout[pos.row][pos.col]
                 collected_on_path.add(pos)
                 path_goals_order.append(pos)
             elif i < len(path) - 1:
                 next_pos = path[i+1]
                 if next_pos.row < pos.row: marker = '^'
                 elif next_pos.row > pos.row: marker = 'v'
                 elif next_pos.col < pos.col: marker = '<'
                 elif next_pos.col > pos.col: marker = '>'
                 else: marker = '*'
             else:
                 marker = '*'
             if pos != self.start_pos and pos != self.exit_pos and pos not in self.goal_positions:
                 if temp_grid[pos.row][pos.col] == '.':
                     temp_grid[pos.row][pos.col] = marker
             elif pos in self.goal_positions:
                  pass
        print("\nPath Found:")
        for r in range(self.rows):
            print(" ".join(temp_grid[r]))
        print(f"\nPath Length: {len(path) - 1} steps")
        if path_goals_order:
            goal_str = " -> ".join([f"Goal@{g}(Prio:{self.goal_priorities.get(g, 'N/A')})" for g in path_goals_order])
            print(f"Goal Collection Order: Start -> {goal_str} -> Exit")
        else:
             print("No goals collected on this path (or no goals defined).")
def reconstruct_path(node: SearchNode) -> List[Point]:
    path = []
    current = node
    while current:
        path.append(current.position)
        current = current.parent
    return path[::-1]
def bfs_search(grid: Grid) -> Optional[List[Point]]:
    start_node = SearchNode(grid.start_pos, frozenset(), 0, None)
    if start_node.position == grid.exit_pos and start_node.collected_goals == grid.all_goals_fs:
        return [start_node.position]
    queue = deque([start_node])
    visited: Set[Tuple[Point, FrozenSet[Point]]] = {start_node.get_state_tuple()}
    nodes_expanded = 0
    while queue:
        current_node = queue.popleft()
        nodes_expanded += 1
        if current_node.position == grid.exit_pos and current_node.collected_goals == grid.all_goals_fs:
            print(f"BFS Nodes Expanded: {nodes_expanded}")
            return reconstruct_path(current_node)
        for next_pos, action in grid.get_neighbors(current_node.position):
            new_collected = set(current_node.collected_goals)
            if next_pos in grid.goal_positions:
                new_collected.add(next_pos)
            new_collected_fs = frozenset(new_collected)
            next_state_tuple = (next_pos, new_collected_fs)
            if next_state_tuple not in visited:
                visited.add(next_state_tuple)
                next_node = SearchNode(
                    position=next_pos,
                    collected_goals=new_collected_fs,
                    cost=current_node.cost + 1,
                    parent=current_node,
                    action=action
                )
                queue.append(next_node)
    print(f"BFS Nodes Expanded: {nodes_expanded}")
    return None
def dfs_search(grid: Grid) -> Optional[List[Point]]:
    start_node = SearchNode(grid.start_pos, frozenset(), 0, None)
    if start_node.position == grid.exit_pos and start_node.collected_goals == grid.all_goals_fs:
        return [start_node.position]
    stack = [start_node]
    visited: Set[Tuple[Point, FrozenSet[Point]]] = {start_node.get_state_tuple()}
    nodes_expanded = 0
    while stack:
        current_node = stack.pop()
        nodes_expanded += 1
        visited.add(current_node.get_state_tuple())
        if current_node.position == grid.exit_pos and current_node.collected_goals == grid.all_goals_fs:
            print(f"DFS Nodes Expanded: {nodes_expanded}")
            return reconstruct_path(current_node)
        for next_pos, action in reversed(grid.get_neighbors(current_node.position)):
            new_collected = set(current_node.collected_goals)
            if next_pos in grid.goal_positions:
                new_collected.add(next_pos)
            new_collected_fs = frozenset(new_collected)
            next_state_tuple = (next_pos, new_collected_fs)
            if next_state_tuple not in visited:
                next_node = SearchNode(
                    position=next_pos,
                    collected_goals=new_collected_fs,
                    cost=current_node.cost + 1,
                    parent=current_node,
                    action=action
                )
                stack.append(next_node)
    print(f"DFS Nodes Expanded: {nodes_expanded}")
    return None
def uniform_cost_search(grid: Grid) -> Optional[List[Point]]:
    start_node = SearchNode(grid.start_pos, frozenset(), 0.0, None)
    if start_node.position == grid.exit_pos and start_node.collected_goals == grid.all_goals_fs:
        return [start_node.position]
    priority_queue = [start_node]
    visited: Set[Tuple[Point, FrozenSet[Point]]] = {start_node.get_state_tuple()}
    min_cost: Dict[Tuple[Point, FrozenSet[Point]], float] = {start_node.get_state_tuple(): 0.0}
    nodes_expanded = 0
    while priority_queue:
        current_node = heapq.heappop(priority_queue)
        nodes_expanded += 1
        current_state_tuple = current_node.get_state_tuple()
        if current_node.cost > min_cost.get(current_state_tuple, float('inf')):
             continue
        if current_node.position == grid.exit_pos and current_node.collected_goals == grid.all_goals_fs:
            print(f"UCS Nodes Expanded: {nodes_expanded}")
            return reconstruct_path(current_node)
        for next_pos, action in grid.get_neighbors(current_node.position):
            move_cost = 1.0
            new_cost = current_node.cost + move_cost
            new_collected = set(current_node.collected_goals)
            if next_pos in grid.goal_positions:
                new_collected.add(next_pos)
            new_collected_fs = frozenset(new_collected)
            next_state_tuple = (next_pos, new_collected_fs)
            if new_cost < min_cost.get(next_state_tuple, float('inf')):
                min_cost[next_state_tuple] = new_cost
                visited.add(next_state_tuple)
                next_node = SearchNode(
                    position=next_pos,
                    collected_goals=new_collected_fs,
                    cost=new_cost,
                    parent=current_node,
                    action=action
                )
                heapq.heappush(priority_queue, next_node)
    print(f"UCS Nodes Expanded: {nodes_expanded}")
    return None
def a_star_search(grid: Grid, heuristic_func) -> Optional[List[Point]]:
    start_node = SearchNode(grid.start_pos, frozenset(), 0.0, None)
    if start_node.position == grid.exit_pos and start_node.collected_goals == grid.all_goals_fs:
        return [start_node.position]
    initial_h_score = heuristic_func(start_node.position, start_node.collected_goals, grid)
    priority_queue = [(start_node.cost + initial_h_score, start_node)]
    g_scores: Dict[Tuple[Point, FrozenSet[Point]], float] = {start_node.get_state_tuple(): 0.0}
    nodes_expanded = 0
    while priority_queue:
        f_score, current_node = heapq.heappop(priority_queue)
        nodes_expanded += 1
        current_state_tuple = current_node.get_state_tuple()
        if current_node.position == grid.exit_pos and current_node.collected_goals == grid.all_goals_fs:
            print(f"A* Nodes Expanded: {nodes_expanded}")
            return reconstruct_path(current_node)
        for next_pos, action in grid.get_neighbors(current_node.position):
            move_cost = 1.0
            new_g_score = current_node.cost + move_cost
            new_collected = set(current_node.collected_goals)
            if next_pos in grid.goal_positions:
                new_collected.add(next_pos)
            new_collected_fs = frozenset(new_collected)
            next_state_tuple = (next_pos, new_collected_fs)
            if new_g_score < g_scores.get(next_state_tuple, float('inf')):
                g_scores[next_state_tuple] = new_g_score
                h_score = heuristic_func(next_pos, new_collected_fs, grid)
                new_f_score = new_g_score + h_score
                next_node = SearchNode(
                    position=next_pos,
                    collected_goals=new_collected_fs,
                    cost=new_g_score,
                    parent=current_node,
                    action=action
                )
                heapq.heappush(priority_queue, (new_f_score, next_node))
    print(f"A* Nodes Expanded: {nodes_expanded}")
    return None
def manhattan_distance(p1: Point, p2: Point) -> int:
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)
def null_heuristic(position: Point, collected: FrozenSet[Point], grid: Grid) -> float:
    return 0.0
def basic_heuristic(position: Point, collected: FrozenSet[Point], grid: Grid) -> float:
    return float(manhattan_distance(position, grid.exit_pos))
def goal_aware_heuristic(position: Point, collected: FrozenSet[Point], grid: Grid) -> float:
    remaining_goals = grid.all_goals_fs - collected
    if not remaining_goals:
        return float(manhattan_distance(position, grid.exit_pos))
    else:
        min_dist_to_goal = float('inf')
        nearest_goal = None
        for goal in remaining_goals:
            dist = manhattan_distance(position, goal)
            if dist < min_dist_to_goal:
                min_dist_to_goal = dist
                nearest_goal = goal
        if nearest_goal:
           dist_to_exit = manhattan_distance(position, grid.exit_pos)
           return float(dist_to_exit + len(remaining_goals))
        else:
             return float(manhattan_distance(position, grid.exit_pos))
if __name__ == "__main__":
    grid_layout_simple = [
        "S.G.#",
        "..#..",
        "..#E.",
        "....."
    ]
    grid_layout_weighted = [
        "S.1.E",
        ".#.#.",
        "..#2.",
        "....."
    ]
    grid_layout_complex = [
        "S.......#",
        "......3.#",
        "...##...#",
        ".1.#....#",
        "...#..#..",
        "......#2.",
        ".####...#",
        "........E"
    ]
    grid_layout_no_path = [
        "S#G",
        "#E#"
    ]
    current_grid_layout = grid_layout_complex
    grid = Grid(current_grid_layout)
    print("Grid Layout:")
    for row in grid.layout:
        print(" ".join(row))
    print(f"Start: {grid.start_pos}, Exit: {grid.exit_pos}")
    print(f"Goals: {grid.goal_positions}")
    print(f"Goal Priorities: {grid.goal_priorities}")
    print("-" * 20)
    algorithms = {
        "BFS": bfs_search,
        "DFS": dfs_search,
        "UCS": uniform_cost_search,
        "A* (Null)": lambda g: a_star_search(g, null_heuristic),
        "A* (Goal Aware)": lambda g: a_star_search(g, goal_aware_heuristic)
    }
    results = {}
    for name, func in algorithms.items():
        print(f"\nRunning {name}...")
        start_time = time.time()
        path = func(grid)
        end_time = time.time()
        duration = end_time - start_time
        print(f"{name} Duration: {duration:.6f} seconds")
        grid.print_path(path)
        results[name] = (path, duration)
        print("-" * 20)
    print("\n--- Analysis ---")
    print("Objective: Collect all goals (G or 1-9) and reach the exit (E).")
    print("\nPath Lengths Found:")
    shortest_len = float('inf')
    fastest_algo_optimal = []
    for name, (path, _) in results.items():
        length = len(path) - 1 if path else "N/A"
        print(f"  {name}: {length}")
        if path and length != "N/A":
             if length < shortest_len:
                 shortest_len = length
                 fastest_algo_optimal = [name]
             elif length == shortest_len:
                 fastest_algo_optimal.append(name)
    if shortest_len != float('inf'):
         print(f"\nShortest path length ({shortest_len} steps) found by: {', '.join(fastest_algo_optimal)}")
         if "DFS" in results and results["DFS"][0] and (len(results["DFS"][0])-1) > shortest_len:
             print("  Note: DFS is not guaranteed to find the shortest path.")
         if "BFS" not in fastest_algo_optimal and "UCS" not in fastest_algo_optimal and "A*" not in fastest_algo_optimal:
             print("  Warning: Expected BFS, UCS, or A* to find the shortest path.")
    else:
        print("\nNo path found by any algorithm (or goals unreachable/exit unreachable after goals).")
    print("\nExecution Times:")
    for name, (_, duration) in results.items():
        print(f"  {name}: {duration:.6f} seconds")
    print("\nTrade-offs between Path Length and Goal Priority:")
    print("  - The current implementations (BFS, UCS, A*) prioritize finding the *shortest path* in terms of steps (cost=1 per move) that collects *all* required goals before reaching the exit.")
    print("  - Goal 'priority' (represented by digits 1-9) is currently *not* affecting the path cost calculated by UCS/A*. It's treated as metadata.")
    print("  - Scenario 1: If priorities mean 'collect higher priority goals sooner if multiple optimal paths exist', the current algorithms don't explicitly do this. Tie-breaking in the priority queue might coincidentally favor certain goals, but it's not guaranteed.")
    print("  - Scenario 2: If priorities represent a 'reward' for collection, the objective function could change to maximize (Total Reward - Path Cost). This would require modifying the cost calculation in UCS/A* (e.g., `new_cost = current_cost + move_cost - reward`) and potentially adjusting the A* heuristic for admissibility.")
    print("  - Scenario 3: If priorities represent a 'cost' for collection (e.g., time penalty), this cost could be *added* to `g(n)` when a goal is first collected. UCS/A* would then minimize (Path Length + Collection Costs).")
    print("  - Scenario 4: If the task was to collect the *highest total priority* within a *limited number of steps*, or find the best path collecting only a *subset* of goals, the problem becomes different (e.g., related to Orienteering Problem or Prize-Collecting TSP), often requiring more complex algorithms or heuristics.")
    print("  - The 'Goal Aware' A* heuristic attempts to guide the search towards remaining goals, which *indirectly* considers their existence, but not their numerical priority value.")
    print("  - Conclusion: For the stated goal (shortest path visiting *all* goals), standard BFS/UCS/A* are suitable. Analyzing priority requires defining how priority impacts the definition of 'optimal' (beyond just path length).")