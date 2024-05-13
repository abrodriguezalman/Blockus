from textwrap import dedent
import pytest

from shape_definitions import ShapeKind
from piece import Piece
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
    s: str = ""
    # Create the top border
    size = len(grid)
    for _ in range(size + 2):
        s += "||"
    s += "\n"
    # Create the rows of the grid
    for row in grid:
        s += "||"
        for cell in row:
            if cell is None:
                s += ". "
            else:
                # Filled cells are represented as the player num and the shape
                # kind. Ensure the shape kind is one letter
                kind = str(cell[1])
                kind = kind.split(".")[1]
                if kind in MULT:
                    i = MULT.index(kind)
                    kind = ONE[i]
                s += f"{cell[0]}{kind}"
        s += "||\n"
    # Create the bottom border
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
    temp = dedent(s).split("\n")
    size = int(len(temp[0])/2 - 2)
    grid: Grid = [[None] * size for _ in range(size)]
    for i, row in enumerate(temp[1:1 + size]):
        found = False
        for j, x in enumerate(row[2:-2]):
            if x not in (".", " "):
                if found:
                    found = False
                    grid[i][int((j - 1) / 2)] = (player_num, ShapeKind(x))
                else:
                    found = True
                    player_num: int = int(x)
    return grid

def test_grid_1() -> None:
    """Test the string to grid and grid to string methods on an empty
    5x5 board"""
    blokus = Blokus(1, 5, {(0, 0), (2, 2), (4, 4)})

    grid = blokus.grid
    s = """
        ||||||||||||||
        ||. . . . . ||
        ||. . . . . ||
        ||. . . . . ||
        ||. . . . . ||
        ||. . . . . ||
        ||||||||||||||
        """
    # Use s[1:-2] to get rid of extra newline characters
    assert dedent(s)[1:-1] == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_2() -> None:
    """Test the string to grid and grid to string methods on a 5x5 board with a
    few pieces played, but only one player."""
    blokus = Blokus(1, 5, {(0, 0), (2, 2), (4, 4)})
    piece_one = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.F])
    piece_two.set_anchor((3, 2))
    assert blokus.maybe_place(piece_two)

    grid = blokus.grid
    s = """
        ||||||||||||||
        ||1O1O. . . ||
        ||1O1O. . . ||
        ||. . 1F1F. ||
        ||. 1F1F. . ||
        ||. . 1F. . ||
        ||||||||||||||
        """
    # Use s[1:-2] to get rid of extra newline characters
    assert dedent(s)[1:-1] == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_3() -> None:
    """Test the string to grid and grid to string methods on a 14x14 board with
    a few pieces played by two players."""
    blokus = Blokus(2, 14, {(4, 4), (9, 9)})
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((9, 9))
    assert blokus.maybe_place(piece_two)

    piece_three = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece_three.set_anchor((6, 6))
    assert blokus.maybe_place(piece_three)

    piece_four = Piece(blokus.shapes[ShapeKind.S])
    piece_four.set_anchor((7, 8))
    assert blokus.maybe_place(piece_four)

    grid = blokus.grid
    s = """
        ||||||||||||||||||||||||||||||||
        ||. . . . . . . . . . . . . . ||
        ||. . . . . . . . . . . . . . ||
        ||. . . . . . . . . . . . . . ||
        ||. . . . . . . . . . . . . . ||
        ||. . . . 11. . . . . . . . . ||
        ||. . . . . 1717. . . . . . . ||
        ||. . . . . . 17. . . . . . . ||
        ||. . . . . . 17. 2S2S. . . . ||
        ||. . . . . . . 2S2S. . . . . ||
        ||. . . . . . . . . 2222. . . ||
        ||. . . . . . . . . . . . . . ||
        ||. . . . . . . . . . . . . . ||
        ||. . . . . . . . . . . . . . ||
        ||. . . . . . . . . . . . . . ||
        ||||||||||||||||||||||||||||||||
        """
    # Use s[1:-2] to get rid of extra newline characters
    assert dedent(s)[1:-1] == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_4() -> None:
    """Test the string to grid and grid to string methods on a 10x10 board.
    Ensure that all shapes with longer than one letter kinds (LETTER_O, ONE,
    TWO, THREE, etc.) are all played correctly"""
    blokus = Blokus(1, 10, {(0, 0), (9, 9)})
    piece_one = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two.set_anchor((2, 2))
    assert blokus.maybe_place(piece_two)

    piece_three = Piece(blokus.shapes[ShapeKind.TWO])
    piece_three.set_anchor((3, 3))
    assert blokus.maybe_place(piece_three)

    piece_four = Piece(blokus.shapes[ShapeKind.THREE])
    piece_four.set_anchor((4, 6))
    assert blokus.maybe_place(piece_four)

    piece_five = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_five.set_anchor((2, 6))
    assert blokus.maybe_place(piece_five)

    piece_six = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_six.set_anchor((6, 2))
    assert blokus.maybe_place(piece_six)

    piece_seven = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece_seven.set_anchor((6, 9))
    assert blokus.maybe_place(piece_seven)

    grid = blokus.grid
    s = """
        ||||||||||||||||||||||||
        ||1O1O. . . . . . . . ||
        ||1O1O. . . . . . . . ||
        ||. . 11. . 14141414. ||
        ||. . . 1212. . . . . ||
        ||. . 15. . 131313. . ||
        ||. . 15. . . . . 1717||
        ||. . 15. . . . . . 17||
        ||. . 15. . . . . . 17||
        ||. . 15. . . . . . . ||
        ||. . . . . . . . . . ||
        ||||||||||||||||||||||||
        """
    # Use s[1:-2] to get rid of extra newline characters
    assert dedent(s)[1:-1] == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_5() -> None:
    """Test the string to grid and grid to string methods on a 10x10 board.
    Ensure that rotation works and players can share edges with other players'
    pieces."""
    blokus = Blokus(2, 10, {(2, 2), (7, 7)})
    piece_one = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_one.set_anchor((3, 2))
    piece_one.rotate_right()
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.L])
    piece_two.set_anchor((7, 5))
    piece_two.flip_horizontally()
    piece_two.rotate_right()
    assert blokus.maybe_place(piece_two)

    piece_three = Piece(blokus.shapes[ShapeKind.TWO])
    piece_three.set_anchor((7, 3))
    piece_three.rotate_left()
    assert blokus.maybe_place(piece_three)

    piece_four = Piece(blokus.shapes[ShapeKind.FOUR])
    piece_four.set_anchor((3, 3))
    piece_four.rotate_right()
    assert blokus.maybe_place(piece_four)

    grid = blokus.grid
    s = """
        ||||||||||||||||||||||||
        ||. . . . . . . . . . ||
        ||. . . . . . . . . . ||
        ||. . 1424. . . . . . ||
        ||. . 1424. . . . . . ||
        ||. . 1424. . . . . . ||
        ||. . 1424. . . . . . ||
        ||. . . 122L. . . . . ||
        ||. . . 122L2L2L2L. . ||
        ||. . . . . . . . . . ||
        ||. . . . . . . . . . ||
        ||||||||||||||||||||||||
        """
    # Use s[1:-2] to get rid of extra newline characters
    assert dedent(s)[1:-1] == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))
