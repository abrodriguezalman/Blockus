from shape_definitions import ShapeKind
from fakes import BlokusFake
from piece import Point, Shape, Piece
from base import BlokusBase, Grid
from blokus import Blokus

import sys
import random
from typing import Optional

times = int(sys.argv[1])

#position randomizer
def rand_pos() -> Point:
    return (random.randint(1, 13), random.randint(1, 13))

def game() -> list[int] | list[None]:
    game = BlokusFake(2, 10, {(0,0), (9,9)})
    
    while not game.game_over:
        #bot 1
        ni_bot(game)

        #bot 2
        s_bot(game)

    return game.winners




def ni_bot(blokus: "BlokusFake") -> None:
    """
    The needs improvement bot. This bot decides which piece to play and where
    on completely random.

    Inputs:
        blokus [BlokusFake]: the fake implementation of blokus that is currently 
            running

    Returns: [None], just plays or retires
        
    """
    avail_moves: set[Piece] = blokus.available_moves()

    if len(avail_moves) != 0:
        for _ in range(len(avail_moves)):
            piece = random.choice(list(avail_moves))
            
            if blokus.maybe_place(piece): 
                return None
        blokus.retire()
        return None
    else:
        blokus.retire()
    return None




def s_bot(blokus: "BlokusFake") -> None:
    """
    Satisfactory bot. Chooses pieces using the function choose_larger, 
    where the bot prefers the play the largest piece it can play.

    Inputs: 
        blokus [BlokusFake]: the blokus game being played
    
    Returns [None]: Just plays or retires
    """
    avail_moves: set[Piece] = blokus.available_moves()
    length = len(avail_moves)
    if length != 0:
        for _ in range(length):
            piece = choose_larger(avail_moves)
            if blokus.maybe_place(piece):
                #print(f"I played a piece: {len(piece.squares())}")
                return None
            else:
                avail_moves.remove(piece)

        blokus.retire()
        return None
    else:

        blokus.retire()
    return None

def choose_larger(pcs: set[Piece]) -> Piece:
    max_squares: int = 0
    max_piece = None
    for piece in pcs: 
        cur_len = len(piece.squares())
        if cur_len == 5:
            return piece
        if cur_len > max_squares:
            max_squares = cur_len
            max_piece = piece
        
    return max_piece

def main() -> None:
    win0 = 0
    win1 = 0
    tie = 0
    for _ in range(times):
        winners = game()
        if len(winners) > 1:
            tie += 1
        elif 1 in winners:
            win0 += 1
        else:
            win1 += 1
    return \
    f"Bot 0 Wins |  {(win0 / times) * 100} %\
    \nBot 1 Wins |  {(win1 / times) * 100} %\
    \nTies       |  {(tie / times) * 100} % \n"

print(main())

#this is a version of s-bot I want to keep in the file
"""
def s2_bot(blokus: "BlokusFake"):
    avail_moves: set[Piece] = blokus.available_moves()
    length = len(avail_moves)
    if length != 0:
        for _ in range(length):
            piece = avail_moves.pop(-1) 
            if blokus.maybe_place(piece):
                print(f"I played a piece: {len(piece.squares())}")
                return None

        blokus.retire()
        return None
    else:

        blokus.retire()
    return None
"""