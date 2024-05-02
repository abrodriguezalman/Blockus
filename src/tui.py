import sys
from fakes import BlokusStub

red: str = "\x1b[1;31m"
blue: str = "\x1b[1;34m"
black: str = "\x1b[1;30m"

sz: int = int(sys.argv[1])
start_positions: set[tuple[int, int]]= {(sz//2 - 1, sz//2 - 1), (sz//2, sz//2)}
stub_game: 'BlokusStub' = BlokusStub(2, sz, start_positions)

def draw_board(game: 'BlokusStub') -> str:
    """
    Draws the board for a given BlokusStub game object.

    Inputs:
        game [BlokusStub]: a Blokus game object
    
    Returns [str]: a string representation of the game board.
    """
    print("┌" + "──┬" * game.size)

    for i, row in enumerate(game.grid):
        board_row: list[str] = []

        for j, cell in enumerate(row):
            if cell is None:
                if (i, j) in start_positions:
                    board_row.append("██" + black)
                else:
                    board_row.append("  ")
            elif cell[0] == 1:
                board_row.append(blue + "██" + black)
            else:
                board_row.append(red + "██" + black)

        print("│" + '│'.join(board_row)+"│")

        if i != game.size - 1:
            print("├──" * game.size + "┤")

    print("└" + "──┴" * game.size)

draw_board(stub_game)
