"""
GUI for Connect Four
"""

import os
import sys
from typing import Union, Optional
import random
import math
import distinctipy
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
Cell = Optional[tuple[int, ShapeKind]]
Grid = list[list[Cell]]

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
    _piece_grid: dict[ShapeKind, bool] #TYPE THIS LATER

    def __init__(self, num: int, blokus: BlokusBase, color: tuple[int, int, int]) -> None:
        self._num = num
        self._blokus = blokus
        self._color = color

        self.set_piece(self.pick_random_piece())

        #create a grid of pieces
        #this will be used to display the remaining pieces visually
        piece_grid = {}
        r = self._blokus.remaining_shapes(self.num)
        for s in self._blokus.shapes:
            piece_grid[s] = s not in r
        
        self._piece_grid = piece_grid

    @property
    def color(self) -> Color:
        return self._color
    
    @property
    def num(self) -> int:
        return self._num
    
    def set_piece(self, p: Piece) -> None:
        self.pending_piece = p
    
    def pick_random_piece(self) -> Piece:
        """pick a random piece for the given player"""

        remaining = self._blokus.remaining_shapes(self.num)
        shapekind = random.choice(remaining)
        shape = self._blokus.shapes[shapekind]
        piece = Piece(shape)
        piece.set_anchor((int(self._blokus.size/2), int(self._blokus.size/2)))

        return piece


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

    #draw the game board
    for row in range(size):
        for col in range(size):
            rect = (row * s + SPACING/2, col * s + SPACING/2, s, s)

            #fill in start positions - black
            if (row, col) in blokus.start_positions:
                pygame.gfxdraw.box(surface, rect, (0, 0, 0))
            
            #if there is a piece on the square, fill in with player's color
            if grid[row][col] is not None:
                p1 = grid[row][col][0]
                color = players[p1-1].color
                pygame.gfxdraw.box(surface, rect, color)

            #draw borders on all squares
            pygame.draw.rect(surface, color=(102, 0, 204),
                                 rect=rect, width=BORDER)
    
    #draw text at the top of the board to indicate which player's turn it is
    p = players[blokus.curr_player-1]
    font = pygame.font.Font(None, 40)
    t = "Player " + str(p.num) + "'s turn"
    text = font.render(t, True, p.color)
    surface.blit(text, ((surface.get_width()-text.get_width())/2, SPACING/8))


    #draw pending piece
    for square in p.pending_piece.squares():
        rect = (square[0] * s + SPACING/2, square[1] * s + SPACING/2, s, s)
        pygame.gfxdraw.box(surface, rect, p.color)
        pygame.draw.rect(surface, color=(0, 0, 0),
                                 rect=rect, width=5*BORDER)
        

    #calculate # of pieces per row
    s_bank = int(1.5*s)     #size of a bank square
    sq_per_row = math.floor((s * blokus.size)/s_bank)
    nrow = math.ceil(21 / sq_per_row)

    row_count = 0
    
    #draw the piece bank
    for i in range(len(p._piece_grid)):
        pi = list(p._piece_grid.keys())[i]
        played = p._piece_grid[pi]

        #location of big square
        #this is the LEFT aligh
        row_place = (i - (row_count * sq_per_row)) * s_bank + SPACING/2
        margin = s * blokus.size - s_bank * sq_per_row + 2*s/5
        row_place += margin
        
        #this is the TOP align
        col_place = s * blokus.size + (0.75 + 0.5 * row_count) * SPACING 
        rect = pygame.Rect((row_place, col_place, s_bank, s_bank))

        if (i+1) % sq_per_row == 0 and i > 0:
            row_count += 1

        #color coding - 
        #player's color for remaining pieces
        #white for pending piece
        #gray for played pieces
        color = p.color
        if played:
            color = (192, 192, 192)
        elif pi == p.pending_piece.shape.kind:
            #pygame.gfxdraw.box(surface, rect, (0,0,0))
            color = (255,255,255)

        #draw each square of the pieces
        for square in blokus.shapes[pi].squares:
            s2 = s/5
            row = row_place + s2 * square[0]
            col = col_place + s2 * square[1]
            rect2 = pygame.Rect((row, col, s2, s2))

            pygame.gfxdraw.box(surface, rect2, color)
            pygame.draw.rect(surface, color=(0, 0, 0),
                                 rect=rect2, width=BORDER)
            
        #code to blit the shape's name rather than the shape
        #text = font.render(pi.value, True, color)
        #cen = text.get_rect(center = rect.center)
        #surface.blit(text, cen)


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

    #determine which side length to use
    s = SIDE * blokus.size
    if blokus.size > 15:
        s = SMALL_SIDE * blokus.size

    #calculate # of pieces per row
    s_bank = int(1.5*(s/blokus.size))    #size of a bank square
    sq_per_row = math.floor((s)/s_bank)
    nrow = math.ceil(21 / sq_per_row)

    surface = pygame.display.set_mode((s + SPACING, s + nrow*s_bank))

    while not blokus.game_over:
        p = players[blokus.curr_player-1]

        # proesss events
        events = pygame.event.get()
        for event in events:
            
            #quit for x-int out
            if event.type == pygame.QUIT:
                #quit for x-ing out
                pygame.quit()
                sys.exit()

            #process keybord events
            elif event.type == pygame.KEYDOWN:
                #quit for escape key
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                #attempt to place piece
                elif event.key == pygame.K_RETURN:
                    if blokus.maybe_place(p.pending_piece):
                        p._piece_grid[p.pending_piece.shape.kind] = True
                        p.set_piece(p.pick_random_piece())
                        #if it is the first piece, remove the chosen start position

                #process arrow key events
                elif event.key == pygame.K_UP:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0], a[1]-1)

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)
                elif event.key == pygame.K_DOWN:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0], a[1]+1)

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)
                elif event.key == pygame.K_RIGHT:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0]+1, a[1])

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)
                elif event.key == pygame.K_LEFT:
                    p2 = p.pending_piece
                    a = p2.anchor
                    a2 = (a[0]-1, a[1])

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a) 


                #process transformations
                #don't currently know the needed keys, so I've just picked some
                """elif event.key == pygame.K_f:
                    p.pending_piece.flip_horizontally()
                elif event.key == pygame.K_l:
                    p.pending_piece.rotate_left()
                elif event.key == pygame.K_r:
                    p.pending_piece.rotate_right()"""

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos

           
        draw_board(surface, blokus, players)
        pygame.display.update()
        clock.tick(24)

#
# Command-line interface
#

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
    col_list = distinctipy.get_colors(blokus.num_players, [(229, 204, 255), (102,0,204)])
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
