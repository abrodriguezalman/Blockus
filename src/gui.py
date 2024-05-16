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
from blokus import Blokus
from shape_definitions import ShapeKind
from piece import Piece
import colorsys
from guibot import SBot

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#constants for drawing the game board
SIDE: int = 40
SMALL_SIDE: int = 35
SMALLER_SIDE: int = 30
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

        #picks a random piece to start with
        self._pending_piece = self.pick_random_piece()

        #dictionary of pieces tracking which pieces the player has played
        #and their corresponding rectangle location in the piece bank
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
        if p.shape not in self._blokus.remaining_shapes(self.num):
            self._pending_piece = p
    
    def pick_random_piece(self) -> Piece:
        """pick a random piece to play from remaining pieces"""

        remaining = self._blokus.remaining_shapes(self.num)
        shapekind = random.choice(remaining)
        shape = self._blokus.shapes[shapekind]
        piece = Piece(shape)
        piece.set_anchor((int(self._blokus.size/2), int(self._blokus.size/2)))

        return piece

def pick_size(blokus: BlokusBase) -> int:
    """Use blokus' size to pick a grid square size

    Input: blokus (BlokusBase) - the blokus game
    """
    if blokus.size >= 17:
        return SMALLER_SIDE
    if blokus.size >= 15:
        return SMALL_SIDE
    return SIDE

def bank_calcs(blokus: BlokusBase, s: int) -> tuple[int, int, int]:
    """Calculate information needed to draw and interact with the piece bank

    Inputs:
        blokus (BlokusBase) - the blokus game
        s (int) - the total size (in pixels) of the blokus board

    Output: tuple[int, int, int]. in order, the tuple contains:
        the size of a piece bank square
        the number of piece bank squares per row
        the number of rows needed to display all pieces
    """
    
    s_bank = int(1.25*(s/blokus.size))
    sq_per_row = math.floor((s)/s_bank)
    nrow = math.ceil(21 / sq_per_row) 

    return (s_bank, sq_per_row, nrow)

def draw_board(surface: pygame.surface.Surface, blokus: BlokusBase, players: list[Player]) -> None:
    """ Draws the current state of the board in the window

    Args:
        surface (pygame.surface.Surface): pygame surface to draw the board on
        blokus (BlokusBase): the blokus game
        players (list[Player]): the list of players

    Returns: None
    """
    grid = blokus.grid
    size = blokus.size

    surface.fill((229, 204, 255))

    #pick a grid-box side length based on size
    s = pick_size(blokus)

    #values for aligning
    board_align_row = surface.get_width()/2 - (s*blokus.size/2)
    board_align_col = surface.get_height()/2 - (s*blokus.size/2)

    #draw the game board
    for row in range(size):
        for col in range(size):
            rect = (row * s + board_align_row, col * s + board_align_col, s,s)
            
            #fill in start positions - black
            if (row, col) in blokus.start_positions:
                pygame.gfxdraw.box(surface, rect, (0, 0, 0))
            
            #if there is a piece on the square, fill in with player's color
            if grid[row][col] is not None:
                p1 = grid[row][col][0]
                color = players[p1-1].color
                pygame.gfxdraw.box(surface, rect, color)

            #draw borders on all grid boxes
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
        rect = (square[0] * s + board_align_row, square[1] * s + board_align_col, s, s)
        pygame.gfxdraw.box(surface, rect, p.color)
        pygame.draw.rect(surface, color=(0, 0, 0),
                                 rect=rect, width=4*BORDER)

    #draw the piece bank
    for player in players:
        draw_piece_grid(surface, blokus, player)

    #draw the game summary - each player will be in a corner
    font = pygame.font.Font(None, 30)
    for p in players:
        x = SPACING/8
        y = SPACING/8

        if p.num % 2 == 0:
            x = surface.get_width() - 1.25*SPACING
        if p.num - 2 <= 0:
            y  = surface.get_height() - 0.75*SPACING

        t = "Player " + str(p.num)
        text = font.render(t, True, p.color)
        surface.blit(text, ((x,y)))

        t = "Score = " + str(blokus.get_score(p.num))
        text = font.render(t, True, p.color)
        surface.blit(text, ((x, y + SPACING/4)))

        if p.num in blokus.retired_players:
            t = "Retired"
            text = font.render(t, True, p.color)
            surface.blit(text, ((x, y + SPACING/2)))


def draw_piece_grid(surface: pygame.surface.Surface, blokus: BlokusBase, p: Player) -> None:
    """draws each player's piece bank

    Inputs: 
        surface (pygame.surface.Surface) - the pygame surface to draw on
        blokus (BlokusBase) - the blokus game
        p (Player) - the player
    """

    #pick the grid size based on blokus size
    s = pick_size(blokus)

    #calculate # of squares of size s_bank that can fit in a single row below the board
    #adjust for smaller blokus boards
    s_bank, sq_per_row, nrow = bank_calcs(blokus, s*blokus.size)
    if blokus.size <= 7:
        sq_per_row += 1
    row_count = 0

    #rectangle representing the board as a whole
    board = pygame.Rect(surface.get_width()/2 - (s*blokus.size/2), surface.get_height()/2 - (s*blokus.size/2), s*blokus.size, s*blokus.size)

    #draw the piece bank
    for i in range(len(p._piece_grid)):
        pi = list(p._piece_grid.keys())[i]
        played = p._piece_grid[pi][0]

        #square to place the mini piece-drawing in
        #this is the LEFT align
        row_place = board.left + (i - (row_count * sq_per_row)) * s_bank
        margin = s * blokus.size - s_bank * sq_per_row
        row_place += margin/2
        
        #adjust TOP (col_place) and LEFT (row_place) align based on the player
        if p.num == 1:
            col_place = board.bottom + s_bank * row_count
        elif p.num == 2:
            col_place = board.right + s_bank * row_count
        elif p.num == 3:
            col_place = board.left - s_bank * (row_count + 1)
        elif p.num == 4:
            col_place = board.top - s_bank * (row_count + 1)
        
        #add the square to the player's _piece_grid
        rect = pygame.Rect((row_place, col_place, s_bank, s_bank))
        if p.num == 1 or p.num == 4:
            p._piece_grid[pi] = (played, rect)
        elif p.num == 2 or p. num == 3:
            rect = pygame.Rect((col_place, row_place, s_bank, s_bank))
            p._piece_grid[pi] = (played, rect)

        #create a new row
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

            rect2: pygame.Rect
            if(p.num == 1):
                rect2 = pygame.Rect((row, col, s2, s2))
            elif(p.num == 2):
                rect2 = pygame.Rect((col, row, s2, s2))
            elif(p.num == 3):
                rect2 = pygame.Rect((col, row, s2, s2))
            elif(p.num == 4):
                rect2 = pygame.Rect((row, col, s2, s2))
            

            pygame.gfxdraw.box(surface, rect2, color)
            pygame.draw.rect(surface, color=(0, 0, 0),
                                 rect=rect2, width=BORDER)


def play_blokus(blokus: BlokusBase, players: list[Player]) -> None:
    """Plays a game of Blokus

    Inputs:
        blokus (BlokusBase): the blokus game
        players (list[Player]): the list of players
    """

    #initalize pygame
    pygame.init()
    pygame.display.set_caption("Blokus!")
    clock = pygame.time.Clock()

    #determine which side length to use
    s = pick_size(blokus) * blokus.size

    #calculate # of pieces per row
    #this is used to determine surface size
    s_bank, sq_per_row, nrow = bank_calcs(blokus, int(s))

    #the pygame surface
    surface = pygame.display.set_mode((s + ((nrow+1) * (s_bank + SPACING/4)) + SPACING/2, s + (nrow-1)*(s_bank + 0.25* SPACING) + 2*SPACING))

    #create rectangle to represent the board
    #and a dictionary mapping keys to shapekinds
    #this will facilitate events later on
    board = pygame.Rect(surface.get_width()/2 - (s/2), surface.get_height()/2 - (s/2), s, s)
    key_dict = {
        pygame.K_1: ShapeKind.ONE,
        pygame.K_2: ShapeKind.TWO,
        pygame.K_3: ShapeKind.THREE,
        pygame.K_4: ShapeKind.FOUR,
        pygame.K_5: ShapeKind.FIVE,
        pygame.K_7: ShapeKind.SEVEN,
        pygame.K_c: ShapeKind.C,
        pygame.K_s: ShapeKind.S,
        pygame.K_o: ShapeKind.LETTER_O,
        pygame.K_a: ShapeKind.A,
        pygame.K_f: ShapeKind.F,
        pygame.K_l: ShapeKind.L,
        pygame.K_n: ShapeKind.N,
        pygame.K_p: ShapeKind.P,
        pygame.K_t: ShapeKind.T,
        pygame.K_u: ShapeKind.U,
        pygame.K_v: ShapeKind.V,
        pygame.K_w: ShapeKind.W,
        pygame.K_x: ShapeKind.X,
        pygame.K_y: ShapeKind.Y,
        pygame.K_z: ShapeKind.Z
    }

    #play the game!
    while not blokus.game_over:
        p = players[blokus.curr_player-1]
        p2 = p.pending_piece
        a = p.pending_piece.anchor

        if p.is_bot:
            if SBot.s_bot(blokus) is None:
                blokus.retire()
            else:
                p.set_piece(SBot.s_bot(blokus))
                blokus.maybe_place(p.pending_piece)
                p._piece_grid[p2.shape.kind] = (True, p._piece_grid[p2.shape.kind][1])

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
                        if len(blokus.remaining_shapes(p.num)) > 0:
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
                
                #retire
                elif event.key == pygame.K_q:
                    blokus.retire()

                #process transformations
                elif event.key == pygame.K_SPACE:
                    p2.flip_horizontally()
                elif event.key == pygame.K_e:
                    p2.rotate_left()
                elif event.key == pygame.K_r:
                    p2.rotate_right()

                #select pieces based on keyboard events
                elif event.key in key_dict:
                    p.set_piece(Piece(blokus.shapes[key_dict[event.key]]))
                    p.pending_piece.set_anchor(a)

            #process clicks
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos

                #click on the grid -> set anchor
                if board.collidepoint(pos):
                    t = s/blokus.size
                    x = math.floor((pos[0]-board.left)/t)
                    y = math.floor((pos[1]-board.top)/t)

                    print((x,y))
                    p2.set_anchor((x,y))
                    if blokus.any_wall_collisions(p2):
                        p2.set_anchor(a)
                
                #click on bank -> choose that piece, if unplayed
                for skind in p._piece_grid:
                    if p._piece_grid[skind][1].collidepoint(pos):
                        if skind in blokus.remaining_shapes(p.num):
                            shape = blokus.shapes[skind]
                            piece = Piece(shape)
                            p.set_piece(piece)
                            p.pending_piece.set_anchor(a)
           
        #update the board
        draw_board(surface, blokus, players)
        pygame.display.update()
        clock.tick(24)

    #if game is over, display winners!!
    while blokus.game_over:
        events = pygame.event.get()
        for event in events:
            
            #quitting
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
        #display winners
        if blokus.winners is not None:
            if len(blokus.winners) == 1:
                t = "Player " + str(blokus.winners[0]) + " wins!"
                col = p.color
            else:
                t = "Players "
                for w in range(len(blokus.winners)-1):
                    t += str(w+1)
                    t += ", "
                t += str(blokus.winners[len(blokus.winners)-1])
                t += " win!"
                col = (0, 0, 0)

            font = pygame.font.Font(None, 70)
            text = font.render(t, True, col)
            cen = text.get_rect(center = board.center)
            surface.blit(text, cen)

            #update board
            pygame.display.update()


#
# Command-line interface
#

@click.command(name="blokus-gui")
@click.option('-n', '--num-players', type=click.INT, default=2)
@click.option('-s', '--size', type=click.INT, default=14)
@click.option('-p', '--start-position', 's_pos', nargs=2, multiple=True, type=click.Tuple([int,int]), default = {(4,4),(9,9)})
@click.option('--game', type=click.Choice(['mono', 'duo', 'classic-2', 'classic-3', 'classic-4']))
@click.option('--bot', is_flag=True)

def cmd(num_players: int, size: str, s_pos: set[tuple[int,int]], game: str, bot: bool = False) -> None:
    """
    Takes in command line input and creates a new blokus game
    """
    blokus: BlokusBase

    #game
    if game is not None:
        if game == "duo":
            blokus = Blokus(num_players, size, s_pos)
        elif game == "mono":
            blokus = Blokus(1, 11, {(5,5)})
        elif "classic" in game:
            size = 20
            s_pos2 = {(0,0), (0,size-1), (size-1,0), (size-1,size-1)}
            if game == "classic-2":
                blokus = Blokus(2, 20, s_pos2)
            elif game == "classic-3":
                blokus = Blokus(3, 20, s_pos2)
            else:
                blokus = Blokus(4, 20, s_pos2)
    else:
        blokus = Blokus(num_players, size, s_pos)

    #create list of players and assign random colors
    players = list()
    for x in range(1, blokus.num_players+1):
        #generate a random color
        #must check for duplicates + make sure color is not border or background color - do later
        
        """col_list = distinctipy.get_colors(10, exclude_colors=[(0,0,0), (1,1,1), (192/255, 192/255, 192/255), (229/255, 204/255, 1), (102/255, 0, 204/255)])
        print(col_list)
        distinctipy.color_swatch(col_list)

        for i in range(len(col_list)):
            col_list[i] = distinctipy.get_rgb256(col_list[i])
        print(col_list)"""

        #generate in HLS first, then convert to RGB-255
        color = (random.randint(0, 360)/360, random.randrange(30, 80)/100, random.randrange(40, 100)/100)
        color = colorsys.hls_to_rgb(color[0], color[1], color[2])
        color = (color[0] * 255, color[1] * 255, color[2] * 255)

        if bot:
            players.append(Player(x, blokus, color, True))
        else:
            players.append(Player(x, blokus, color))

    play_blokus(blokus, players)

if __name__ == "__main__":
        cmd()
