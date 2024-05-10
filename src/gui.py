"""
GUI for Connect Four
"""

import os
import sys
from typing import Union, Optional
import random
import math
import pygame
import pygame.gfxdraw
import click
from base import BlokusBase
from fakes import BlokusStub, BlokusFake
from blokus import Blokus
from shape_definitions import ShapeKind
from piece import Piece
from guibot import NIBot


os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#constants for drawing the game board
SIDE: int = 45
SMALL_SIDE: int = 35
BORDER: int = 1
SPACING: int = 100

#data types
Color = tuple[int, int, int]
Cell = Optional[tuple[int, ShapeKind]]
Grid = list[list[Cell]]

#class to store player information
class Player:
    """
    Class to store information about each player in the GUI
    """

    _num: int
    _blokus: BlokusBase
    _color: Color
    _pending_piece: Piece | None
    _piece_grid: dict[ShapeKind, (bool, pygame.Rect | None)]
    is_bot: bool
    bot: NIBot | None

    def __init__(self, num: int, blokus: BlokusBase, color: tuple[int, int, int], is_bot: bool = False) -> None:
        """Constructor
        
        Inputs:
            num (int): the player's number
            blokus (BlokusBase): the blokus game
            color (Color): the player's randomly generated color
        
            IN PROGRESS:
            is_bot (bool): whether or not the player is a bot (defaults to False)"""

        self._num = num
        self._blokus = blokus
        self._color = color
        self.is_bot = is_bot

        if is_bot:
            self.bot = NIBot()
        else:
            self.bot = None

        #picks a pending piece (at this point random)
        self._pending_piece = self.pick_random_piece()

        #create a dictionary of pieces tracking which pieces the player has played
        #this will be used to display the remaining pieces visually
        piece_grid = {}
        r = self._blokus.remaining_shapes(self.num)
        for s in self._blokus.shapes:
            piece_grid[s] = (s not in r, None)
        
        self._piece_grid = piece_grid

    @property
    def color(self) -> Color:
        return self._color
    
    @property
    def num(self) -> int:
        return self._num

    @property
    def pending_piece(self) -> Piece | None:
        return self._pending_piece
    
    def set_piece(self, p: Piece) -> None:
        """Sets the pending pieces to the input piece
        
        Input: p (Piece) - the new piece
        """
        p.set_anchor(self.pending_piece.anchor)
        self._pending_piece = p
    
    def pick_random_piece(self) -> Piece:
        """pick a random piece to play"""

        remaining = self._blokus.remaining_shapes(self.num)
        shapekind = random.choice(remaining)
        shape = self._blokus.shapes[shapekind]
        piece = Piece(shape)
        piece.set_anchor((int(self._blokus.size/2), int(self._blokus.size/2)))

        return piece

def pick_size(blokus: BlokusBase) -> int:
    if blokus.size >= 15:
        return SMALL_SIDE
    return SIDE

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

    #pick a grid-box side length based on size
    s = pick_size(blokus)

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

    #draw the pending piece
    #the pending piece will have a thicker black border
    for square in p.pending_piece.squares():
        rect = (square[0] * s + SPACING/2, square[1] * s + SPACING/2, s, s)
        pygame.gfxdraw.box(surface, rect, p.color)
        pygame.draw.rect(surface, color=(0, 0, 0),
                                 rect=rect, width=4*BORDER)

    #draw the piece bank
    draw_piece_grid(surface, blokus, p)

    #draw the retire button
    rect = pygame.Rect(surface.get_width() - 2*s, surface.get_height() - s, 2*s, s)
    pygame.gfxdraw.box(surface, rect, p.color)
    font = pygame.font.Font(None, 30)
    t = "Retire"

    #pick black or white text depending on color
    if (p.color[0]*0.299 + p.color[1]*0.587 + p.color[2]*0.114) > 186:
        text = font.render(t, True, (0,0,0))
    else:
        text = font.render(t, True, (255, 255, 255))

    cen = text.get_rect(center = rect.center)
    surface.blit(text, cen)



def draw_piece_grid(surface: pygame.surface.Surface, blokus: BlokusBase, p: Player) -> None:

    s = pick_size(blokus)

    #calculate # of squares of size s_bank that can fit in a single row below the board
    s_bank = int(1.25*s)     
    sq_per_row = math.floor((s * blokus.size)/s_bank)
    row_count = 0
    
    #draw the piece bank
    for i in range(len(p._piece_grid)):
        pi = list(p._piece_grid.keys())[i]
        played = p._piece_grid[pi][0]

        #square to place the mini piece-drawing in
        #this is the LEFT aligh
        row_place = (i - (row_count * sq_per_row)) * s_bank + SPACING/2
        margin = s * blokus.size - s_bank * sq_per_row
        row_place += margin/2
        
        #this is the TOP align
        col_place = s * blokus.size + s_bank * row_count + SPACING/2
        rect = pygame.Rect((row_place, col_place, s_bank, s_bank))
        p._piece_grid[pi] = (played, rect)

        #new row
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

        #draw a mini version of each piece
        for square in blokus.shapes[pi].squares:
            s2 = s/5
            row = row_place + s2 * square[0] + rect.width/2
            col = col_place + s2 * square[1] + rect.height/2
            rect2 = pygame.Rect((row, col, s2, s2))

            pygame.gfxdraw.box(surface, rect2, color)
            pygame.draw.rect(surface, color=(0, 0, 0),
                                 rect=rect2, width=BORDER)
            

def play_blokus(blokus: BlokusBase, players: list[Player]) -> None:
    """Plays a game of Blokus

    Inputs:
        blokus: the blokus game
        players: a list of players
    """

    #initalize pygame
    pygame.init()
    pygame.display.set_caption("Blokus!")
    clock = pygame.time.Clock()

    #determine which side length to use
    s = SIDE * blokus.size
    if blokus.size >= 15:
        s = SMALL_SIDE * blokus.size

    #calculate # of pieces per row
    #this is used to determine surface size
    s_bank = int(1.25*(s/blokus.size))    #size of a bank square
    sq_per_row = math.floor((s)/s_bank)
    nrow = math.ceil(21 / sq_per_row) 

    surface = pygame.display.set_mode((s + SPACING, s + nrow * s_bank + SPACING*.75))

    #create rectangles to represent the grid and piece bank
    #this will facilitate mouse events later on
    board = pygame.Rect(SPACING/2, SPACING/2, s, s)
    bank = pygame.Rect(SPACING/2, s + 0.5 * SPACING, s, math.ceil(21 / sq_per_row)  * s_bank)
    retire = pygame.Rect(surface.get_width() - 2*s, surface.get_height() - s, 2*s, s)

    #play the game!
    while not blokus.game_over:
        p = players[blokus.curr_player-1]
        p2 = p.pending_piece
        a = p.pending_piece.anchor

        #proesss pygame events
        events = pygame.event.get()
        for event in events:
            
            #quit for x-ing out
            if event.type == pygame.QUIT:
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
                    if blokus.maybe_place(p2):

                        #update piece_grid and pick a new pending piece
                        p._piece_grid[p2.shape.kind] = (True, p._piece_grid[p2.shape.kind][1])
                        p.set_piece(p.pick_random_piece())

                #process arrow key events (moving the pending piece)
                elif event.key == pygame.K_UP:
                    a2 = (a[0], a[1]-1)

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)

                elif event.key == pygame.K_DOWN:
                    a2 = (a[0], a[1]+1)

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)

                elif event.key == pygame.K_RIGHT:
                    a2 = (a[0]+1, a[1])

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)

                elif event.key == pygame.K_LEFT:
                    a2 = (a[0]-1, a[1])

                    p2.set_anchor(a2)
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a) 

                #process transformations
                #don't currently know the needed keys, so I've just picked some
                elif event.key == pygame.K_f:
                    p2.flip_horizontally()
                elif event.key == pygame.K_l:
                    p2.rotate_left()
                elif event.key == pygame.K_r:
                    p2.rotate_right()

            #process clicks
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos

                #click on the grid -> set anchor
                if board.collidepoint(pos):
                    t = s/blokus.size
                    (x,y) = (int(pos[0]/t)-1, int(pos[1]/t)-1)
                    
                    p2.set_anchor((x,y))
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)
                
                #click on bank -> choose piece
                elif bank.collidepoint(pos):
                    for skind in p._piece_grid:
                        if p._piece_grid[skind][1].collidepoint(pos):
                            shape = blokus.shapes[skind]
                            piece = Piece(shape)
                            p.set_piece(piece)

                #retire
                elif retire.collidepoint(pos):
                    blokus.retire()

           
        draw_board(surface, blokus, players)
        pygame.display.update()
        clock.tick(24)

    #if game is over, display winners!!
    if blokus.winners is not None:
        font = pygame.font.Font(None, 40)
        t = "Player " + str(blokus.winners[0]) + " wins!"
        text = font.render(t, True, p.color)
        surface.blit(text, ((surface.get_width()/2, surface.get_height()/2)))

    draw_board(surface, blokus, players)
    pygame.display.update()
    clock.tick(24)
    


def play_blokus_bot(blokus: BlokusBase, players: list[Player]) -> None:
    """Plays a game of blokus between bots

    Args:
        blokus: the blokus game
        players: list of players

    This method is currently (5/8/24) nonfunctional
    """
    
    #initalize pygame
    pygame.init()
    pygame.display.set_caption("Blokus!")
    clock = pygame.time.Clock()

    #determine which side length to use
    s = SIDE * blokus.size
    if blokus.size >= 15:
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

        pygame.time.wait(int(0.5*1000))
        p.set_piece(p.bot.ni_bot(blokus, blokus.available_moves()))
        blokus.maybe_place(p.pending_piece)
        p._piece_grid[p.pending_piece.shape.kind] = True

        draw_board(surface, blokus, players)
        pygame.display.update()
        clock.tick(24)


#
# Command-line interface
#

def cmd(size: int, mode: str, bot: bool = False) -> None:
    """
    Takes in command line input and creates a new blokus game
    """
    blokus: BlokusBase
    num: int = 4
    s_pos: set[tuple[int, int]]

    #determine size and start positions based on mono or duo
    if mode == "duo":
        size = 14
        num = 2
        s_pos = {(4,4), (9,9)}
    elif mode == "mono":
        size = 11
        s_pos = {(5,5)}
        num = 1
    else:
        s_pos = {(0,0), (0,size-1), (size-1,0), (size-1,size-1)}

    blokus = Blokus(num, size, s_pos)

    #create list of players and assign random colors
    players = list()
    for x in range(1, blokus.num_players+1):
        #generate a random color
        #must check for duplicates + make sure color is not border or background color - do later
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if bot:
            players.append(Player(x, blokus, color, True))
        else:
            players.append(Player(x, blokus, color))

    if bot:
        play_blokus_bot(blokus, players)
    else:
        play_blokus(blokus, players)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "duo" or sys.argv[1] == "mono":
            cmd(0, sys.argv[1])
        elif sys.argv[1] == "bot":
            cmd(14, "", True)
        else:
            cmd(int(sys.argv[1]), "")
    else:
        cmd()
