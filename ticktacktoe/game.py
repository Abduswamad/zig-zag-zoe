from abc import ABC, abstractmethod

class Game(ABC):
    def __init__(self, board, player1, player2):
        self.board = board()
        self.player1 = player1
        self.player2 = player2

    @abstractmethod
    def play(self):
        pass


class TicTacToe(Game):
    def play(self):
        current_player = self.player1
        while True:
            self.board.display()
            if current_player.make_move(self.board):
                if self.board.is_winner(current_player.symbol):
                    self.board.display()
                    print(f"Player {current_player.symbol} wins!")
                    break
                if self.board.is_full():
                    self.board.display()
                    print("The game is a draw!")
                    break
                current_player = self.player2 if current_player == self.player1 else self.player1