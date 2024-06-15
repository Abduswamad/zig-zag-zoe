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
