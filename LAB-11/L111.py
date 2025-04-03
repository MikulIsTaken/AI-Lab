import itertools
import heapq
from collections import deque


class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9  # 3x3 board represented as a list
        self.current_player = 'X'

    def display_board(self):
        for i in range(0, 9, 3):
            print(self.board[i], '|', self.board[i + 1], '|', self.board[i + 2])
        print("-" * 9)

    def get_valid_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def is_winner(self, player):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        return any(all(self.board[i] == player for i in combo) for combo in winning_combinations)

    def is_draw(self):
        return ' ' not in self.board

    def make_move(self, move, player):
        if self.board[move] == ' ':
            self.board[move] = player
            return True
        return False

    def undo_move(self, move):
        self.board[move] = ' '

    def heuristic(self, board, player):
        if self.is_winner('X'):
            return 10
        elif self.is_winner('O'):
            return -10
        return 0

    def a_star_move(self):
        best_move = None
        best_score = float('-inf')
        for move in self.get_valid_moves():
            self.board[move] = 'O'
            score = self.minimax(False)
            self.undo_move(move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, is_max):
        if self.is_winner('O'):
            return 10
        if self.is_winner('X'):
            return -10
        if self.is_draw():
            return 0

        if is_max:
            best_score = float('-inf')
            for move in self.get_valid_moves():
                self.board[move] = 'O'
                score = self.minimax(False)
                self.undo_move(move)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_valid_moves():
                self.board[move] = 'X'
                score = self.minimax(True)
                self.undo_move(move)
                best_score = min(best_score, score)
            return best_score

    def bfs_move(self):
        queue = deque([(self.board[:], move) for move in self.get_valid_moves()])
        while queue:
            state, move = queue.popleft()
            return move  # Pick the first valid move found

    def dfs_move(self):
        stack = [(self.board[:], move) for move in self.get_valid_moves()]
        while stack:
            state, move = stack.pop()
            return move  # Pick the last valid move found

    def play_game(self):
        print("Welcome to Tic-Tac-Toe!")
        self.display_board()

        while True:
            if self.current_player == 'X':
                move = int(input("Enter your move (0-8): "))
                if move not in self.get_valid_moves():
                    print("Invalid move. Try again.")
                    continue
            else:
                print("Choose AI Strategy: 1. BFS 2. DFS 3. A*")
                choice = input("Enter 1, 2, or 3: ")
                if choice == '1':
                    move = self.bfs_move()
                elif choice == '2':
                    move = self.dfs_move()
                else:
                    move = self.a_star_move()
                print(f"AI chooses position: {move}")

            self.make_move(move, self.current_player)
            self.display_board()

            if self.is_winner(self.current_player):
                print(f"{self.current_player} wins!")
                break
            if self.is_draw():
                print("It's a draw!")
                break

            self.current_player = 'O' if self.current_player == 'X' else 'X'


# Start game
game = TicTacToe()
game.play_game()