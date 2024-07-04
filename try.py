import tkinter as tk
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, symbol):
        self.symbol = symbol

    @abstractmethod
    def make_move(self, board):
        pass


class HumanPlayer(Player):
    def make_move(self, board):
        if len(board.moves[self.symbol]) < 3:
            while True:
                try:
                    row, col = map(int, input(f"Enter row and column to place {self.symbol} (0-2 0-2): ").split())
                    if 0 <= row <= 2 and 0 <= col <= 2:
                        if board.update_board(row, col, self.symbol):
                            return True
                        else:
                            print("Cell is already occupied. Try again.")
                    else:
                        print("Invalid input. Row and column must be between 0 and 2.")
                except ValueError:
                    print("Invalid input. Please enter numbers for row and column.")
        else:
            while True:
                try:
                    row, col = map(int, input(f"Enter row and column to remove {self.symbol} (0-2 0-2): ").split())
                    if 0 <= row <= 2 and 0 <= col <= 2:
                        if board.remove_move(row, col, self.symbol):
                            print(f"Removed {self.symbol} from ({row}, {col}). Now place your new move.")
                            break
                        else:
                            print("Invalid move. You can only remove your own pieces. Try again.")
                    else:
                        print("Invalid input. Row and column must be between 0 and 2.")
                except ValueError:
                    print("Invalid input. Please enter numbers for row and column.")
            while True:
                try:
                    row, col = map(int, input(f"Enter row and column to place {self.symbol} (0-2 0-2): ").split())
                    if 0 <= row <= 2 and 0 <= col <= 2:
                        if board.update_board(row, col, self.symbol):
                            return True
                        else:
                            print("Cell is already occupied. Try again.")
                    else:
                        print("Invalid input. Row and column must be between 0 and 2.")
                except ValueError:
                    print("Invalid input. Please enter numbers for row and column.")


class AIPlayer(Player):
    def make_move(self, board):
        if len(board.moves[self.symbol]) < 3:
            best_move = self.minimax(board, self.symbol)['position']
            board.update_board(best_move[0], best_move[1], self.symbol)
            return True
        else:
            best_score = -float('inf')
            move_to_remove = None

            for move in board.moves[self.symbol]:
                # Temporarily remove the move and evaluate
                board.remove_move(move[0], move[1], self.symbol)
                move_score = self.minimax(board, self.symbol)['score']
                if move_score > best_score:
                    best_score = move_score
                    move_to_remove = move
                # Restore the move
                board.update_board(move[0], move[1], self.symbol)

            if move_to_remove:
                board.remove_move(move_to_remove[0], move_to_remove[1], self.symbol)
                print(f"AI removed {self.symbol} from ({move_to_remove[0]}, {move_to_remove[1]}).")

            best_move = self.minimax(board, self.symbol)['position']
            board.update_board(best_move[0], best_move[1], self.symbol)
            return True

    def minimax(self, board, player):
        opponent = 'O' if player == 'X' else 'X'

        if board.is_winner(self.symbol):
            return {'position': None, 'score': 1}  # AI wins
        elif board.is_winner(opponent):
            return {'position': None, 'score': -1}  # Opponent wins
        elif board.is_full():
            return {'position': None, 'score': 0}  # Draw

        if player == self.symbol:
            best = {'position': None, 'score': -float('inf')}  # Maximize AI
        else:
            best = {'position': None, 'score': float('inf')}  # Minimize opponent

        for cell in board.get_empty_cells():
            board.update_board(cell[0], cell[1], player)
            sim_score = self.minimax(board, opponent)
            board.remove_move(cell[0], cell[1], player)
            sim_score['position'] = cell

            if player == self.symbol:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best


class Board:
    def __init__(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.moves = {'X': [], 'O': []}

    def update_board(self, row, col, symbol):
        if self.board[row][col] == '':
            self.board[row][col] = symbol
            self.moves[symbol].append((row, col))
            return True
        return False

    def remove_move(self, row, col, symbol):
        if self.board[row][col] == symbol:
            self.board[row][col] = ''
            self.moves[symbol].remove((row, col))
            return True
        return False

    def is_winner(self, symbol):
        # Check rows, columns, and diagonals for a win
        for row in self.board:
            if all(cell == symbol for cell in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == symbol for row in range(3)):
                return True
        if all(self.board[i][i] == symbol for i in range(3)) or all(self.board[i][2 - i] == symbol for i in range(3)):
            return True
        return False

    def is_full(self):
        return all(cell != '' for row in self.board for cell in row)

    def get_empty_cells(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == '']


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = Board()
        self.current_player = HumanPlayer('X')
        self.ai_player = AIPlayer('O')
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_widgets()

    def create_widgets(self):
        for r in range(3):
            for c in range(3):
                button = tk.Button(self.root, text='', font='normal 20 bold', height=3, width=6,
                                   command=lambda r=r, c=c: self.on_button_click(r, c))
                button.grid(row=r, column=c)
                self.buttons[r][c] = button

    def on_button_click(self, row, col):
        if self.board.update_board(row, col, self.current_player.symbol):
            self.buttons[row][col].config(text=self.current_player.symbol)
            if self.check_game_over(self.current_player.symbol):
                return
            self.current_player = self.ai_player if self.current_player == self.current_player else self.current_player
            self.ai_move()

    def ai_move(self):
        self.current_player.make_move(self.board)
        self.update_buttons()
        if self.check_game_over(self.current_player.symbol):
            return
        self.current_player = HumanPlayer('X')

    def update_buttons(self):
        for r in range(3):
            for c in range(3):
                if self.board.board[r][c] == 'X':
                    self.buttons[r][c].config(text='X')
                elif self.board.board[r][c] == 'O':
                    self.buttons[r][c].config(text='O')
                else:
                    self.buttons[r][c].config(text='')

    def check_game_over(self, symbol):
        if self.board.is_winner(symbol):
            self.show_message(f"{symbol} wins!")
            return True
        elif self.board.is_full():
            self.show_message("It's a draw!")
            return True
        return False

    def show_message(self, message):
        top = tk.Toplevel(self.root)
        top.title("Game Over")
        msg = tk.Message(top, text=message, font='normal 20 bold')
        msg.pack()
        button = tk.Button(top, text="OK", command=self.root.quit)
        button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()
