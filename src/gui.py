"""
GUI for Connect Four
"""

import os
import sys
from typing import Union
import random
import pygame
import pygame.gfxdraw
import click
from base import BlokusBase
from fakes import BlokusStub, BlokusFake
from shape_definitions import ShapeKind
from piece import Piece
#from bot import RandomBot, SmartBot


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#number of pixels for each grid square
SIDE: int = 45
SMALL_SIDE: int = 35
BORDER: int = 1
SPACING: int = 100

Color = tuple[int, int, int]

#class to store player information
class Player:
    """
    Class to store information about each player in the GUI

    Inputs:
        _num (int): the player's number
        _blokus (BlokusBase): the blokus game
        _color (Color): the player's randomly generated color
    """

    _num: int
    _blokus: BlokusBase
    _color: Color
    pending_piece: Piece | None

    def __init__(self, num: int, blokus: BlokusBase, color: tuple[int, int, int]) -> None:
        self._num = num
        self._blokus = blokus
        self._color = color

        #for user event testing only, hardcode the piece
        self.pending_piece = Piece(blokus.shapes[ShapeKind.Z])
        self.pending_piece.set_anchor((int(blokus.size/2), int(blokus.size/2)))

    @property
    def color(self) -> Color:
        return self._color
    
    @property
    def num(self) -> int:
        return self._num
    
    def set_piece(self, p: Piece) -> None:
        self.pending_piece = p


def draw_board(surface: pygame.surface.Surface, blokus: BlokusBase, players: list[Player]) -> None:
    """ Draws the current state of the board in the window

    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw
        players: the list of players

    Returns: None

    """
    grid = blokus.grid
    size = blokus.size

    surface.fill((229, 204, 255))

    s = SIDE
    if blokus.size > 15:
        s = SMALL_SIDE

    # Draw the borders around each cell
    #for now, each cell will be 20px
    for row in range(size):
        for col in range(size):
            rect = (col * s + SPACING/2, row * s + SPACING/2, s, s)

            if (row, col) in blokus.start_positions:
                #fill in start positions
                pygame.gfxdraw.box(surface, rect, (0, 0, 0))
            if grid[row][col] is not None:
                #if there is a piece on the square, fill in with player's color
                p1 = grid[row][col][0]
                color = players[p1-1].color
                pygame.gfxdraw.box(surface, rect, color)

            #draw borders on all squares
            pygame.draw.rect(surface, color=(102, 0, 204),
                                 rect=rect, width=BORDER)
    
    #draw text at the top of the board to indicate which player's turn it is
    font = pygame.font.Font(None, 40)
    t = "Player " + str(blokus.curr_player) + "'s turn"
    text = font.render(t, True, (0, 0, 0))
    surface.blit(text, ((surface.get_width()-text.get_width())/2, SPACING/8))

    #draw pending piece
    p = players[blokus.curr_player-1]
    for square in p.pending_piece.squares():
        rect = (square[0] * s + SPACING/2, square[1] * s + SPACING/2, s, s)
        pygame.gfxdraw.box(surface, rect, p.color)
        pygame.draw.rect(surface, color=(0, 0, 0),
                                 rect=rect, width=5*BORDER)


def play_blokus(blokus: BlokusBase, players: list[Player]) -> None:
    """Plays a game of Blokus

    Inputs:
        blokus: the blokus game
        players: a list of players
    
    As of 4/28/24, the game is not playable.
    Calling this method only draws the blokus board using BlokusStub implementation
    """

    #initalize pygame
    pygame.init()
    pygame.display.set_caption("Blokus!")
    clock = pygame.time.Clock()

    s = SIDE * blokus.size
    if blokus.size > 15:
        s = SMALL_SIDE * blokus.size

    surface = pygame.display.set_mode((s + SPACING, s + SPACING))
    

    while not blokus.game_over:
        p = players[blokus.curr_player-1]

        # proesss events
        events = pygame.event.get()
        for event in events:

            if event.type == pygame.QUIT:
                #quit for x-ing out
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                #process keyboard events
                if event.key == pygame.K_ESCAPE:
                    #quit for esc key
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_KP_ENTER:
                    #attempt to place piece
                    try:
                        blokus.maybe_place(p.pending_piece)
                        #add code to actually place the piece here
                        #remember to update blokus.grid accordingly
                        #if it is the first piece, remove the chosen start position
                    except:
                        pass
                
                #process arrow key events
                elif event.key == pygame.K_UP:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0], a[1]-1)

                    p2.set_anchor(a2)
                    if not blokus.legal_to_place(p2):
                        p2.set_anchor(a)
                elif event.key == pygame.K_DOWN:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0], a[1]+1)

                    p2.set_anchor(a2)
                    if not blokus.legal_to_place(p2):
                        p2.set_anchor(a)
                elif event.key == pygame.K_RIGHT:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0]+1, a[1])

                    p2.set_anchor(a2)
                    if not blokus.legal_to_place(p2):
                        p2.set_anchor(a)
                elif event.key == pygame.K_LEFT:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0]-1, a[1])

                    p2.set_anchor(a2)
                    if not blokus.legal_to_place(p2):
                        p2.set_anchor(a)    
           
        draw_board(surface, blokus, players)
        pygame.display.update()
        clock.tick(24)

#
# Command-line interface
#

#command line options/arguments

def cmd(size: int, mode: str) -> None:
    """
    Takes in command line input and creates a new blokus game
    """
    blokus: BlokusBase
    num: int = 2
    s_pos: set[tuple[int, int]]

    #determine things based on mono or duo
    if mode == "duo":
        size = 14
        s_pos = {(4,4), (9,9)}
    elif mode == "mono":
        size = 11
        s_pos = {(5,5)}
        num = 1
    else:
        s_pos = {(0,0), (0,size-1), (size-1,0), (size-1,size-1)}

    blokus = BlokusFake(num, size, s_pos)

    #create list of players and assign random colors
    players = list()
    for x in range(1, blokus.num_players+1):
        #generate a random color
        #must check for duplicates + make sure color is not border or background color - do later
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        players.append(Player(x, blokus, color))

    play_blokus(blokus, players)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "duo" or sys.argv[1] == "mono":
            cmd(0, sys.argv[1])
        else:
            cmd(int(sys.argv[1]), "")
    else:
        cmd()
