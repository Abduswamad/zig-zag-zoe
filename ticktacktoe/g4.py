class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.board = Board()
        self.human_player = HumanPlayer('X')
        self.ai_player = AIPlayer('O')
        self.current_player = self.human_player
        self.human_needs_to_place = False
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
        if self.current_player == self.human_player:
            if not self.human_needs_to_place:
                if len(self.board.moves[self.current_player.symbol]) < 3:
                    if self.board.update_board(row, col, self.current_player.symbol):
                        self.buttons[row][col].config(text=self.current_player.symbol)
                        if self.check_game_over(self.current_player.symbol):
                            return
                        self.current_player = self.ai_player
                        self.ai_move()
                else:
                    if self.board.board[row][col] == self.current_player.symbol:
                        self.board.remove_move(row, col, self.current_player.symbol)
                        self.update_buttons()
                        self.human_needs_to_place = True
            else:
                if self.board.update_board(row, col, self.current_player.symbol):
                    self.buttons[row][col].config(text=self.current_player.symbol)
                    self.human_needs_to_place = False
                    if self.check_game_over(self.current_player.symbol):
                        return
                    self.current_player = self.ai_player
                    self.ai_move()

    def ai_move(self):
        self.ai_player.make_move(self.board)
        self.update_buttons()
        if self.check_game_over(self.ai_player.symbol):
            return
        self.current_player = self.human_player

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
