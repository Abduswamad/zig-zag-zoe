from ticktacktoe.player import HumanPlayer, AIPlayer
from ticktacktoe.board import Board
from ticktacktoe.game import TicTacToe

def main():
    print("------ TICK TACK TOE GAME --------")
    player1 = HumanPlayer('X')
    player2 = AIPlayer('O')
    game = TicTacToe(Board, player1, player2)
    game.play()
    print("------ TICK TACK TOE GAME --------")


if __name__ == "__main__":
    main()
