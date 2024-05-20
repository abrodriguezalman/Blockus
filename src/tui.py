import curses
import random
import click
from typing import Any
from blokus import Blokus
from shape_definitions import ShapeKind
from piece import Piece, Point

ESC = 27
ENTER_KEYS = [10, 13]
curses.set_escdelay(25)

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
    game: Blokus
    color: Any
    pending_piece: Piece

    def __init__(self, n: int, game: Blokus) -> None:
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
        new_piece = Piece(pp_shape)
        new_piece.set_anchor((self.game.size // 2, self.game.size // 2))

        return new_piece

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
    game: Blokus
    screen: Any
    players: dict[int, TUI_player]

    def __init__(self, game: Blokus) -> None:
        self.game = game
        self.screen = curses.initscr()
        self.players = {}
        curses.start_color()
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
            x [int]: the vertical position where to print the string
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
        curses.resize_term(100, 100)

        grid_color: Any = curses.color_pair(8)
        empty: Any = curses.color_pair(9)
        grid = self.game.grid
        size: int = len(grid)
        curr_player = self.game.curr_player
        pp_sqrs: list[Point] = self.players[curr_player].pending_piece.squares()

        row = 0
        for i in range(1, size * 2, 2):
            col = 0
            
            if i == 1:
                self._print("┌" + "──┬" * size, grid_color, i - 1)
            self._print("│", grid_color, i)

            for j in range(1, size + 1):
                cell = grid[row][col]

                if (row, col) in pp_sqrs:
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
            if player.n in self.game.retired_players:
                self._print(f"Player {player.n} (RETIRED):", player.color, (row + 1) * 2)
            else:
                self._print(f"Player {player.n} (ACTIVE):", player.color, (row + 1) * 2)
            self._print(" ", curses.COLOR_BLACK)

            for shape in self.game.shapes.keys():
                if shape in self.game.remaining_shapes(player.n):
                    if shape == player.pending_piece.shape.kind \
                    and self.game.curr_player == player.n:
                        self._print(shape.value, curses.A_BLINK | player.color)
                    else:
                        self._print(shape.value, player.color)
                else:
                    self._print(shape.value, grid_color)
                self._print(" ", curses.COLOR_BLACK)
            
            self._print(f"Score: {self.game.get_score(player.n)}", player.color)
            row += 1

        if self.game.game_over:
            if self.game.winners is None:
                self._print(f"NONE WON!", grid_color, (row + 1) * 2)
            else:
                winners = ', '.join(f"PLAYER {p}" for p in self.game.winners)
                self._print(f"{winners} WON!", grid_color, (row + 1) * 2)
        
        self.screen.refresh()

def play_blokus(game: 'Blokus') -> None:
    """
    Executes the blokus game loop event.

    Inputs:
        blokus [BlokusFake]: the blokus game

    Returns [None]: Nothing, just executes the game
    """
    blokus = TUI_game(game)
    players = blokus.players
    blokus.screen.keypad(True)

    while not blokus.game.game_over:
        blokus.draw_board()
        curr_player: 'TUI_player' = players[blokus.game.curr_player]
        curr_player_ppiece: 'Piece'= curr_player.pending_piece
        curr_anchor: tuple[int, int] | None = curr_player_ppiece.anchor

        chr_dict: dict[str, ShapeKind] = \
        {shapek.value.lower(): shapek for shapek in blokus.game.shapes.keys()}

        assert not curr_anchor is None
        x, y = curr_anchor
        c = blokus.screen.getch()

        if c == ESC:
            curses.endwin()
            break

        if c == curses.KEY_UP:
            anchor = curr_anchor
            curr_player_ppiece.set_anchor((x - 1, y))
            if blokus.game.any_wall_collisions(curr_player_ppiece):
                curr_player_ppiece.set_anchor(anchor)

        if c == curses.KEY_DOWN:
            anchor = curr_anchor
            curr_player_ppiece.set_anchor((x + 1, y))
            if blokus.game.any_wall_collisions(curr_player_ppiece):
                curr_player_ppiece.set_anchor(anchor)

        if c == curses.KEY_LEFT:
            anchor = curr_anchor
            curr_player_ppiece.set_anchor((x, y - 1))
            if blokus.game.any_wall_collisions(curr_player_ppiece):
                curr_player_ppiece.set_anchor(anchor)

        if c == curses.KEY_RIGHT:
            anchor = curr_anchor
            curr_player_ppiece.set_anchor((x, y + 1))
            if blokus.game.any_wall_collisions(curr_player_ppiece):
                curr_player_ppiece.set_anchor(anchor)

        if c in ENTER_KEYS:
            if blokus.game.maybe_place(curr_player_ppiece):
                curr_player.pending_piece =\
                 curr_player.create_piece(curr_player.random_shape())
        
        for chr, shape in chr_dict.items():
            if c == ord(chr):
                if shape in blokus.game.remaining_shapes(curr_player.n):
                    curr_player.pending_piece = curr_player.create_piece(shape)

        if c == ord("r"):
            curr_player.pending_piece.rotate_right()
            if blokus.game.any_wall_collisions(curr_player_ppiece):
                curr_player.pending_piece.rotate_left()
        
        if c == ord("e"):
            curr_player.pending_piece.rotate_left()
            if blokus.game.any_wall_collisions(curr_player_ppiece):
                curr_player.pending_piece.rotate_right()

        if c == ord(' '):
            curr_player.pending_piece.flip_horizontally()
            if blokus.game.any_wall_collisions(curr_player_ppiece):
                curr_player.pending_piece.flip_horizontally()

        if c == ord("q"):
            blokus.game.retire()
            if blokus.game.game_over:
                blokus.draw_board()

@click.command()
@click.option('-n', '--num-players', type = click.INT, default=2)
@click.option('-s', '--size', type = click.INT, default = 14)
@click.option('-p','--start-position', nargs = 2, type = click.INT, multiple = True, default = [(4, 4), (9,9)])
@click.option('--game', type = click.STRING, default = None)
def cmd(num_players: int, size: int, start_position: int, game: str):
    if not game is None:
        if game == "mono":
            blokusx = Blokus(1, 11, {(5, 5)})
        elif game == "duo":
            blokusx = Blokus(2, 14, {(4, 4), (9,9)})
        elif 'classic-' in game:
            n = int(game[-1])
            blokusx = Blokus(n, 20, {(0, 0), (0,19), (19, 0), (19, 19)})
    else:
        blokusx = Blokus(num_players, size, set(p for p in start_position))
    
    play_blokus(blokusx)

if __name__ == "__main__":
    cmd()
    curses.endwin()
