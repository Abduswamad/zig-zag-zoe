class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.moves = {'X': [], 'O': []}

    def display(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)

    def update_board(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            self.moves[player].append((row, col))
            return True
        return False

    def remove_move(self, row, col, player):
        if (row, col) in self.moves[player]:
            self.board[row][col] = ' '
            self.moves[player].remove((row, col))
            return True
        return False

    def is_winner(self, player):
        # Check rows, columns, and diagonals
        for i in range(3):
            if all([self.board[i][j] == player for j in range(3)]) or \
                    all([self.board[j][i] == player for j in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or \
                all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def get_empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def clone(self):
        clone_board = Board()
        clone_board.board = [row[:] for row in self.board]
        clone_board.moves = {player: moves[:] for player, moves in self.moves.items()}
        return clone_board

    def is_full(self):
        return all([cell != ' ' for row in self.board for cell in row])
