import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Tuple

WIDTH = 10
HEIGHT = 10
MINES = 12
CELL = 30

def init_board(width: int, height: int) -> List[List[str]]:
    return [["." for _ in range(width)] for _ in range(height)]

def place_mines(width: int, height: int, mines: int) -> List[List[bool]]:
    grid = [[False for _ in range(width)] for _ in range(height)]
    placed = 0
    while placed < mines:
        r = random.randrange(height)
        c = random.randrange(width)
        if not grid[r][c]:
            grid[r][c] = True
            placed += 1
    return grid

def neighbors(r: int, c: int, width: int, height: int) -> List[Tuple[int, int]]:
    coords = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                coords.append((nr, nc))
    return coords

def reveal(board: List[List[str]], mines: List[List[bool]], r: int, c: int) -> bool:
    if board[r][c] != ".":
        return True
    if mines[r][c]:
        board[r][c] = "*"
        return False
    count = sum(1 for nr, nc in neighbors(r, c, len(board[0]), len(board)) if mines[nr][nc])
    board[r][c] = str(count) if count else " "
    if count == 0:
        for nr, nc in neighbors(r, c, len(board[0]), len(board)):
            reveal(board, mines, nr, nc)
    return True

def check_win(board: List[List[str]], mines: List[List[bool]]) -> bool:
    for r in range(len(board)):
        for c in range(len(board[0])):
            if not mines[r][c] and board[r][c] == ".":
                return False
    return True

class MinesweeperGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Minesweeper")
        self.board = init_board(WIDTH, HEIGHT)
        self.mines = place_mines(WIDTH, HEIGHT, MINES)
        self.buttons: List[List[tk.Button]] = []
        self.flags: List[List[bool]] = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self._build_grid()

    def _build_grid(self) -> None:
        for r in range(HEIGHT):
            row_buttons = []
            for c in range(WIDTH):
                btn = tk.Button(self, width=4, height=2, command=lambda r=r, c=c: self._on_click(r, c))
                btn.bind("<Button-3>", lambda event, r=r, c=c: self._on_right_click(r, c))
                btn.grid(row=r, column=c)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def _on_click(self, r: int, c: int) -> None:
        if self.flags[r][c]:
            return
        
        safe = reveal(self.board, self.mines, r, c)
        self._update_buttons()
        
        if not safe:
            self._game_over(False)
        elif check_win(self.board, self.mines):
            self._game_over(True)

    def _on_right_click(self, r: int, c: int) -> None:
        if self.board[r][c] != ".":
            return
        
        self.flags[r][c] = not self.flags[r][c]
        btn = self.buttons[r][c]
        if self.flags[r][c]:
            btn.config(text="F", fg="red")
        else:
            btn.config(text="", fg="black")

    def _update_buttons(self) -> None:
        for r in range(HEIGHT):
            for c in range(WIDTH):
                val = self.board[r][c]
                btn = self.buttons[r][c]
                if val != ".":
                    btn.config(text=val, state="disabled", relief="sunken")
                    if val == "*":
                        btn.config(bg="red")

    def _game_over(self, won: bool) -> None:
        # Reveal all mines
        for r in range(HEIGHT):
            for c in range(WIDTH):
                if self.mines[r][c]:
                    self.buttons[r][c].config(text="*", bg="red")
        
        msg = "You Win!" if won else "Game Over!"
        messagebox.showinfo("Minesweeper", msg)
        self.destroy()

if __name__ == "__main__":
    app = MinesweeperGUI()
    app.mainloop()
