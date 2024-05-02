import sys
from fakes import BlokusStub

red: str = "\x1b[1;31m"
blue: str = "\x1b[1;34m"
black: str = "\x1b[1;30m"

size: int = int(sys.argv[1])
start_positions: set[tuple[int, int]]= {(size//2 - 1, size//2 - 1), (size//2, size//2)}
game: 'BlokusStub' = BlokusStub(2, size, start_positions)

def draw_board(game: 'BlokusStub') -> str:
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
        
        if i != size - 1:
            print("├──" * size + "┤")
    
    print("└" + "──┴" * game.size)

draw_board(game)