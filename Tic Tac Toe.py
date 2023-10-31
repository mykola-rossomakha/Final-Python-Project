import tkinter as tk
from tkinter import messagebox
import pickle

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = 'X'
        self.buttons = [[None, None, None] for _ in range(3)]
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.moves = 0

        for row in range(3):
            for col in range(3):
                button = tk.Button(root, text='', width=10, height=3,
                                  command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        self.load_button = tk.Button(root, text="Load Game", command=self.load_game)
        self.load_button.grid(row=4, column=0)
        self.save_button = tk.Button(root, text="Save Game", command=self.save_game)
        self.save_button.grid(row=4, column=1)

    def make_move(self, row, col):
        if self.buttons[row][col]['text'] == '' and self.board[row][col] == '':
            self.buttons[row][col]['text'] = self.current_player
            self.board[row][col] = self.current_player
            self.moves += 1
            if self.check_winner(row, col):
                messagebox.showinfo("Tic-Tac-Toe", f"Player {self.current_player} wins!")
                self.reset_board()
            elif self.is_full():
                messagebox.showinfo("Tic-Tac-Toe", "It's a tie!")
                self.reset_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self, row, col):
        player = self.board[row][col]
        # Check row
        if all(self.board[row][c] == player for c in range(3)):
            return True
        # Check column
        if all(self.board[r][col] == player for r in range(3)):
            return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_full(self):
        return self.moves == 9

    def reset_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]['text'] = ''
                self.board[row][col] = ''
        self.current_player = 'X'
        self.moves = 0

    def save_game(self):
        with open("tic_tac_toe_save.pkl", "wb") as file:
            pickle.dump(self.board, file)

    def load_game(self):
        try:
            with open("tic_tac_toe_save.pkl", "rb") as file:
                self.board = pickle.load(file)
                self.moves = sum(1 for row in self.board for cell in row if cell != '')
                for row in range(3):
                    for col in range(3):
                        self.buttons[row][col]['text'] = self.board[row][col]
        except FileNotFoundError:
            messagebox.showinfo("Tic-Tac-Toe", "No saved game found.")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
