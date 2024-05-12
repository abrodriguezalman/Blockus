import pytest

from shape_definitions import ShapeKind
from piece import Shape, Piece
from base import BlokusBase
from blokus import Blokus
from blokus import Grid

MULT = ["ONE", "TWO", "THREE", "FOUR", "FIVE", "SEVEN", "LETTER_O"]
ONE = ["1", "2", "3", "4", "5", "7", "O"]

def grid_to_string(grid: Grid) -> str:
    """
    Returns a string representation of a Blokus grid.

    Inputs:
        grid [Grid]: the grid to represent

    Returns [str]: a string representation of the grid.    
    """
    s: str = "   "
    size = len(grid)
    for n in range(size):
        s += f"{n} "
    s += "\n "
    for _ in range(size + 2):
        s += "||"
    s += "\n"
    for n, row in enumerate(grid):
        s += f"{n}||"
        for cell in row:
            if cell is None:
                s += ". "
            else:
                kind = str(cell[1])
                kind = kind.split(".")[1]
                if kind in MULT:
                    i = MULT.index(kind)
                    kind = ONE[i]
                s += f"{cell[0]}{kind}"
        s += "||\n"
    s += " "
    for _ in range(size + 2):
        s += "||"

    return s

def string_to_grid(s: str) -> Grid:
    """
    Creates a grid from a string.
    
    Inputs:
        s [str]: the string to transform

    Returns [Grid]: the grid version of the string.
    """
    temp = s.replace(" ", "").split("\n")
    size = int(len(temp[1])/2 - 2)
    grid = [[None] * size for _ in range(size)]
    for i, row in enumerate(temp[2:2 + size]):
        found = False
        for j, x in enumerate(row[3:-2]):
            if x != ".":
                if found:
                    found = False
                    grid[i][int((j - 1) / 2)] = (int(player_num), ShapeKind(x))
                else:
                    found = True
                    player_num = x
    return grid
