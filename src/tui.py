import curses
import sys
import random
from piece import Piece
from fakes import BlokusStub, BlokusFake
from blokus import Blokus
from shape_definitions import ShapeKind
from piece import Piece

def colors() -> None:
    #creates random colors for players
    for i in range(1, 6):
        curses.init_pair(i, random.randint(i, 6), curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE) #grid color pair
    curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_WHITE)#empty space color pair
    
class TUI_player():
    """
    has: player number (1, 2, 3, etc), player designated color pair, and player
    pending piece
    """
    def __init__(self, n: int, game: 'BlokusFake') -> None:
        self.n = n
        self.color = curses.color_pair(n)
        pp_shapekind = random.choice(game.remaining_shapes(n))
        pp_shape = game.shapes[pp_shapekind]
        self.pending_piece = Piece(pp_shape)
        self.pending_piece.set_anchor((game.size // 2, game.size // 2))

class TUI_game():
    """
    has: blockus game, the screen for the game, and all players of the game
    """
    def __init__(self, game: 'BlokusFake') -> None:
        self.game = game
        self.screen = curses.initscr()
        curses.start_color()
        self.players = {}
        
        colors()
        for i in range (1, self.game.num_players + 1):
            self.players[i] = TUI_player(i, self.game)

    def get_player(self, num: int) -> 'TUI_player':
        return self.players[num]

    def _print(self, string: str, color: int, in_position: bool = True, \
                                x: int = 0, y: int = 0) -> None:
        """
        prints out the given stuff to the tui_game screen
        """
        #(0,0) placement is hardcoded rn, to be changed
        if in_position:
            self.screen.addstr(string, color)
        else:
            self.screen.addstr(x, y, string, color)

    def draw_board(self) -> None:
        
        grid_color = curses.color_pair(8)
        n = len(self.game.grid)

        self._print("┌" + "──┬" * n, grid_color)
        r = 0
        for i in range(1, n * 2, 2):
            c = 0
            cell = self.game.grid[r][c]
            self._print("│", grid_color, False, i)
            for j in range(1, n + 1):
                if cell is None:
                    if (r, c) in self.game.start_positions:
                        self._print("██", grid_color)
                    else:
                        self._print("  ", curses.color_pair(9))
                elif (r, c) in self.players[self.game.curr_player].pending_piece.squares():
                    self._print("██", grid_color)
                else:
                    self._print("██", self.get_player(cell[0]).color)
                self._print("│", grid_color)
                c += 1
            if i < (n * 2) - 1:
                self._print("├──" * j + "│", grid_color, False, i + 1)
            else:
                self._print("└" + "──┴" * n, grid_color, False, i + 1)
            r += 1
        #raise NotImplementedError

def play_blokus(blokus: 'BlokusFake') -> None:
    TUI_blockus = TUI_game(blokus)
    players = TUI_blockus.players

    while not TUI_blockus.game.game_over:
        TUI_blockus.draw_board()
        c = TUI_blockus.screen.getch()

        if c == 27: #ESC
            break

#def main() -> None:
    #curses.wrapper(play_blokus)

if __name__ == "__main__":
    #main()
    size: int = int(sys.argv[1])
    blokusx = BlokusFake(2, size, {(0,0),(0,size - 1),(size -1,0),(size - 1,size - 1)})
    play_blokus(blokusx)
