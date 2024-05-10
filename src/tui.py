import curses
import sys
import random
from typing import Any
from fakes import BlokusFake
from shape_definitions import ShapeKind
from piece import Piece, Point

ESC = 27
ENTER_KEYS = [10, 13]

def colors() -> None:
    """
    Creates random color pairs for TUI players and sets game grid color values
        in the curses library.

    Inputs:
        None

    Returns [None]: Does not return, only sets color pairs.
    """
    color_list = list(range(1,6))
    for i in range(1, 6):
        n = random.choice(color_list)
        curses.init_pair(i, n, curses.COLOR_BLACK)
        color_list.remove(n)

    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_BLACK)

class TUI_player():
    """
    Class to represent a TUI Blockus Player.
    """
    n: int
    game: BlokusFake
    color: Any
    pending_piece: Piece

    def __init__(self, n: int, game: BlokusFake) -> None:
        self.n = n
        self.game = game
        self.color = curses.color_pair(n)
        self.pending_piece = self.create_piece(self.random_shape())

    def create_piece(self, sh: ShapeKind) -> Piece:
        """
        Creates a pending piece for the TUI player using a given shapekind.

        Inputs:
            sh [ShapeKind]: a ShapeKind object

        Returns [Piece]: a Piece object
        """
        pp_shape = self.game.shapes[sh]
        pending_piece = Piece(pp_shape)
        pending_piece.set_anchor((self.game.size // 2, self.game.size // 2))

        return pending_piece

    def random_shape(self) -> ShapeKind:
        """
        Returns a random shapekind from the player's remaining shapes.
        
        Inputs:
            None

        Returns [ShapeKind]: A ShapeKind object
        """
        return random.choice(self.game.remaining_shapes(self.n))


class TUI_game():
    """
    Class for representing a TUI Blokus game.
    """
    game: BlokusFake
    screen: Any
    players: dict[int, TUI_player]

    def __init__(self, game: BlokusFake) -> None:
        self.game = game
        self.screen = curses.initscr()
        curses.start_color()
        self.players = {}

        colors()
        for i in range (1, self.game.num_players + 1):
            self.players[i] = TUI_player(i, self.game)

    def get_player(self, num: int) -> TUI_player:
        """
        Returns the TUI Player object for the given player.

        Inputs:
            num: the player number

        Returns [TUI_Player]: the corresponding TUI player object
        """
        return self.players[num]

    def _print(self, string: str, color: int, x: int = 0) -> None:
        """
        Prints the given string in color to the screen, optionally with a
        desired position on the screen.

        Inputs:
            string [str]: the string to be printed
            color [int]: the color for the printed string
            x [int]: the horizontal position where to print the string
                to the screen

        Returns [None]: Nothing, just prints to screen.
        """
        if x == 0:
            self.screen.addstr(string, color)
        else:
            self.screen.addstr(x, 0, string, color)

    def draw_board(self) -> None:
        """
        Draws the current state of the Blokus game board to the screen.

        Inputs:
            None

        Returns [None]: Nothing, just prints to screen.
        """
        self.screen.clear()

        grid_color: Any = curses.color_pair(8)
        empty: Any = curses.color_pair(9)
        grid = self.game.grid
        size: int = len(grid)
        curr_player = self.game.curr_player
        pp_sqrs: list[Point] = self.players[curr_player].pending_piece.squares()

        row = 0
        for i in range(1, size * 2, 2):
            if i == 1:
                self._print("┌" + "──┬" * size, grid_color, i - 1)
            col = 0
            self._print("│", grid_color, i)

            for j in range(1, size + 1):
                cell = grid[row][col]

                if (row,col) in pp_sqrs:
                    self._print("▒▒", \
                    curses.A_BLINK | self.get_player(curr_player).color)
                elif cell is None:
                    if (row, col) in self.game.start_positions:
                        self._print("██", grid_color)
                    else:
                        self._print("  ", empty)
                else:
                    self._print("██", self.get_player(cell[0]).color)
                self._print("│", grid_color)
                col += 1

            if i < (size * 2) - 1:
                self._print("├──" * j + "│", grid_color, i + 1)
            else:
                self._print("└" + "──┴" * size, grid_color, i + 1)
            row += 1

        for player in self.players.values():
            self._print(f"Player {player.n}:", player.color, (row + 1) * 2)
            self._print(" ", curses.COLOR_BLACK)

            for shape in self.game.shapes.keys():
                if shape in self.game.remaining_shapes(player.n):
                    self._print(shape.value, player.color)
                else:
                    self._print(shape.value, curses.COLOR_WHITE)
                self._print(" ", curses.COLOR_BLACK)

            row += 1

        self.screen.refresh()

def play_blokus(blokus: 'BlokusFake') -> None:
    """
    Executes the blokus game loop event.

    Inputs:
        blokus [BlokusFake]: the blokus game

    Returns [None]: Nothing, just executes the game
    """
    blockus = TUI_game(blokus)
    players = blockus.players
    blockus.screen.keypad(True)

    while not blockus.game.game_over:
        blockus.draw_board()
        current_player: 'TUI_player' = players[blockus.game.curr_player]
        current_player_ppiece: 'Piece'= current_player.pending_piece
        current_anchor: tuple[int, int] | None = current_player_ppiece.anchor

        assert not current_anchor is None
        x, y = current_anchor
        c = blockus.screen.getch()

        if c == ESC:
            break

        if c == curses.KEY_UP:
            anchor = current_anchor
            current_player_ppiece.set_anchor((x - 1, y))
            if blockus.game.any_wall_collisions(current_player_ppiece):
                current_player_ppiece.set_anchor(anchor)

        if c == curses.KEY_DOWN:
            anchor = current_anchor
            current_player_ppiece.set_anchor((x + 1, y))
            if blockus.game.any_wall_collisions(current_player_ppiece):
                current_player_ppiece.set_anchor(anchor)

        if c == curses.KEY_LEFT:
            anchor = current_anchor
            current_player_ppiece.set_anchor((x, y - 1))
            if blockus.game.any_wall_collisions(current_player_ppiece):
                current_player_ppiece.set_anchor(anchor)

        if c == curses.KEY_RIGHT:
            anchor = current_anchor
            current_player_ppiece.set_anchor((x, y + 1))
            if blockus.game.any_wall_collisions(current_player_ppiece):
                current_player_ppiece.set_anchor(anchor)

        if c in ENTER_KEYS:
            if blockus.game.maybe_place(current_player_ppiece):
                current_player.pending_piece =\
                 current_player.create_piece(current_player.random_shape())

if __name__ == "__main__":
    mode: str = sys.argv[1]
    try:
        int(mode)
    except:
        if mode == 'mono':
            blokusx = BlokusFake(1, 11, {(5, 5)})
        if mode == 'duo':
            blokusx = BlokusFake(2, 14, {(4, 4), (9,9)})
    else:
        m = int(mode)
        blokusx = BlokusFake(2, m, {(0,0),(0,m - 1),(m -1,0),(m - 1,m - 1)})

    play_blokus(blokusx)
