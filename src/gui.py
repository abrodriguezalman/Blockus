"""
GUI for Connect Four
"""

import os
import sys
from typing import Union
import random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.gfxdraw
import click

from base import BlokusBase
from fakes import BlokusStub, BlokusFake
#from bot import RandomBot, SmartBot

#number of pixels for each grid square
SIDE: int = 50
SMALL_SIDE: int = 40
BORDER: int = 1

Color = tuple[int, int, int]

#class to store player information
class Player:

    _num: int
    _blokus: BlokusBase
    _color: Color

    def __init__(self, num: int, blokus: BlokusBase, color: tuple[int, int, int]) -> None:
        self._num = num
        self._blokus = blokus
        self._color = color

    @property
    def color(self) -> Color:
        return self._color
    
    @property
    def num(self) -> int:
        return self._num


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
            rect = (col * s, row * s, s, s)

            if (row, col) in blokus.start_positions:
                #fill in start positions
                pygame.gfxdraw.box(surface, rect, (0, 0, 0))
            elif grid[row][col] is not None:
                #if there is a piece on the square, fill in with player's color
                #as of now, just make it white
                p1 = grid[row][col][0]
                color = players[p1-1].color
                pygame.gfxdraw.box(surface, rect, color)

            #draw borders on all squares
            pygame.draw.rect(surface, color=(102, 0, 204),
                                 rect=rect, width=BORDER)


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

    s = SIDE * blokus.size
    if blokus.size > 15:
        s = SMALL_SIDE * blokus.size

    surface = pygame.display.set_mode((s, s))
    clock = pygame.time.Clock()

    while not blokus.game_over:
        # proesss events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #PROCESS OTHER EVENTS HERE

        draw_board(surface, blokus, players)
        pygame.display.update()
        clock.tick(24)

#
# Command-line interface
#

#command line options/arguments
@click.command(name="gui")
@click.option('--num_players', type=click.INT, default=2)
@click.argument('size', type=click.INT, default=14)

def cmd(size: int, num_players: int) -> None:
    blokus: BlokusBase
    print(size)

    #temporary start positions - at opposize corners of the board
    #eventually will need to implement this based on board size
    #and account for player colors
    s_pos = {(0,0), (size-1,size-1)}

    #current implementaton uses stub - adapt to fake later
    blokus = BlokusStub(num_players, size, s_pos)

    #create list of players and assign random colors
    players = list()
    for x in range(blokus.num_players):
        #generate a random color
        #must check for duplicates + make sure color is not border or background color - do later
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        players.append(Player(x, blokus, color))

    play_blokus(blokus, players)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd(sys.argv[1:])
    else:
        cmd()
