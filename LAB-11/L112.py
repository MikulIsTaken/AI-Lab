import time
import heapq
from collections import deque
import random


class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.move_history = []

    def print_board(self):
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i + 1]} | {self.board[i + 2]} ")
            if i < 6:
                print("-----------")
        print()

    def make_move(self, position):
        if 0 <= position < 9 and self.board[position] == ' ':
            self.board[position] = self.current_player
            self.move_history.append(position)
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def undo_move(self):
        if self.move_history:
            position = self.move_history.pop()
            self.board[position] = ' '
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def is_winner(self, player):
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(self.board[i] == player for i in pattern) for pattern in win_patterns)

    def is_draw(self):
        return ' ' not in self.board

    def get_legal_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def clone(self):
        new_game = TicTacToe()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.move_history = self.move_history.copy()
        return new_game


# BFS Implementation
def bfs_ai(game):
    start_time = time.time()
    queue = deque([(game.clone(), [])])
    visited = set()
    best_move = None

    while queue:
        current_game, path = queue.popleft()
        board_tuple = tuple(current_game.board)

        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        if current_game.is_winner('X'):
            best_move = path[0] if path else None
            break

        for move in current_game.get_legal_moves():
            new_game = current_game.clone()
            new_game.make_move(move)
            new_path = path + [move]
            queue.append((new_game, new_path))

    print(f"BFS Time: {time.time() - start_time:.5f}s")
    return best_move or random.choice(game.get_legal_moves())


# DFS Implementation
def dfs_ai(game, max_depth=9):
    start_time = time.time()
    best_move = None
    best_score = -float('inf')

    def dfs_evaluate(state, depth):
        nonlocal best_score, best_move
        if state.is_winner('X'):
            return 10 - depth
        if state.is_winner('O'):
            return depth - 10
        if state.is_draw() or depth >= max_depth:
            return 0

        scores = []
        for move in state.get_legal_moves():
            state.make_move(move)
            scores.append(dfs_evaluate(state.clone(), depth + 1))
            state.undo_move()

        return max(scores) if state.current_player == 'X' else min(scores)

    for move in game.get_legal_moves():
        game.make_move(move)
        score = dfs_evaluate(game.clone(), 1)
        game.undo_move()

        if score > best_score:
            best_score = score
            best_move = move

    print(f"DFS Time: {time.time() - start_time:.5f}s")
    return best_move or random.choice(game.get_legal_moves())


# A* Implementation
def a_star_ai(game):
    start_time = time.time()

    def heuristic(state):
        score = 0
        win_patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for pattern in win_patterns:
            values = [state.board[i] for i in pattern]
            x_count = values.count('X')
            o_count = values.count('O')

            if x_count == 3: score += 100
            if o_count == 3: score -= 100
            if x_count == 2 and o_count == 0: score += 10
            if o_count == 2 and x_count == 0: score -= 10
            if x_count == 1 and o_count == 0: score += 1
            if o_count == 1 and x_count == 0: score -= 1

        if state.board[4] == 'X':
            score += 3
        elif state.board[4] == 'O':
            score -= 3

        return score

    heap = []
    initial_state = game.clone()
    heapq.heappush(heap, (-heuristic(initial_state), initial_state, []))
    visited = set()
    best_move = None

    while heap:
        h, current_state, path = heapq.heappop(heap)
        board_tuple = tuple(current_state.board)

        if board_tuple in visited:
            continue
        visited.add(board_tuple)

        if current_state.is_winner('X'):
            best_move = path[0] if path else None
            break

        if current_state.is_draw():
            continue

        for move in current_state.get_legal_moves():
            new_state = current_state.clone()
            new_state.make_move(move)
            new_path = path + [move]
            heapq.heappush(heap, (-heuristic(new_state), new_state, new_path))

    print(f"A* Time: {time.time() - start_time:.5f}s")
    return best_move or random.choice(game.get_legal_moves())


def compare_algorithms():
    test_cases = [
        ['X', 'O', ' ', ' ', 'X', ' ', 'O', ' ', ' '],
        ['X', ' ', 'O', ' ', ' ', ' ', ' ', ' ', ' '],
        ['X', 'O', 'X', 'O', 'X', 'O', ' ', ' ', ' ']
    ]

    for i, board in enumerate(test_cases, 1):
        game = TicTacToe()
        game.board = board.copy()
        game.current_player = 'X'

        print(f"\nTest Case {i}:")
        game.print_board()

        print("BFS Choice:", bfs_ai(game.clone()))
        print("DFS Choice:", dfs_ai(game.clone()))
        print("A* Choice:", a_star_ai(game.clone()))
        print("-------------------")


def play_game():
    game = TicTacToe()
    algorithms = {
        'X': a_star_ai,
        'O': bfs_ai
    }

    while not game.is_winner('X') and not game.is_winner('O') and not game.is_draw():
        game.print_board()
        current_ai = algorithms[game.current_player]
        move = current_ai(game.clone())
        game.make_move(move)

    game.print_board()
    if game.is_winner('X'):
        print("X (A*) wins!")
    elif game.is_winner('O'):
        print("O (BFS) wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    while True:
        print("\nTic-Tac-Toe AI Menu:")
        print("1. Play against AI")
        print("2. Compare algorithms")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            play_game()
        elif choice == '2':
            compare_algorithms()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
