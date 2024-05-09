import curses
import sys
import random
from typing import Any
from fakes import BlokusFake

def colors() -> None:
    #creates random colors for players
    for i in range(1, 7):
        curses.init_pair(i, random.randint(i, 7), curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE) #grid color pair
    
class TUI_player():
    """
    has: player number (1, 2, 3, etc), player designated color pair, and player
    pending piece
    """
    def __init__(self, n: int, game: 'BlokusFake') -> None:
        self.n = n
        self.color = curses.color_pair(n)
        self.pending_piece = random.choice(game.remaining_shapes(n)) #currently a shape
        #a piece is a shape WITH an anchor!

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
            self.players[f"player {i}"] = TUI_player(i, self.game)

    def _print(self, string: str, color: int, x: int = 0, y: int = 0) -> None:
        """
        prints out the given stuff to the tui_game screen
        """
        #(0,0) placement is hardcoded rn, to be changed
        self.screen.addstr(x, y, string, color)

    def draw_board(self) -> None:
        
        nrows = len(self.game.grid)
        ncols = len(self.game.grid)

        self._print("┌" + "──┬" * self.game.size, curses.color_pair(8))
        
        #raise NotImplementedError

def play_blokus() -> None:
    # Parameters to be determined
    raise NotImplementedError

def cmd(size: int) -> None:
    #correct parameters to be determined
    #this is where game will be initialized
    #blokusx = BlokusFake(2, size, {(0,0),(1,1),(2,2),(3,3)})
    #play_blokus(blokusx)
    raise NotImplementedError

#if __name__ == "__main__":
    #cmd()

#testing screen
test_blockus = BlokusFake(2, 5, {(0, 0), (0, 1), (1, 0),(1, 1)})
test_TUI = TUI_game(test_blockus)
test_TUI.draw_board()
test_TUI.screen.refresh()