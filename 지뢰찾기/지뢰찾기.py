import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Tuple |

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
