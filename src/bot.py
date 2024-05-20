from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase, Grid
from blokus import Blokus

import sys
import random
from typing import Optional
import click




def game(player1: str, player2: str) -> list[int] | None:
    game = Blokus(2, 10, {(0,0), (9,9)})
    
    while not game.game_over:
        #player 1 (indexed as 0)
        choose_bot(player1, game)

        #player 2 (indexed as 1)
        choose_bot(player2, game)

    return game.winners

"""
for i, elem in enumerate(sys.argv):
    if elem == "-1":
        players[0] = sys.argv[i + 1]
    if elem == "-2":
        players[1] = sys.argv[i+1]
"""

#position randomizer
def rand_pos() -> Point:
    return (random.randint(1, 13), random.randint(1, 13))


def choose_bot(bot: str, game: "Blokus"):
    if bot == "S":
        s_bot(game)
    if bot == "N": 
        ni_bot(game)
    if bot == "U":
        u_bot(game)
    if bot == "":
        ni_bot(game)


def ni_bot(blokus: "Blokus") -> None:
    """
    The needs improvement bot. This bot decides which piece to play and where
    on completely random.

    Inputs:
        blokus [Blokus]: the implementation of blokus that is currently 
            running

    Returns: [None], just plays or retires
        
    """
    avail_moves: set[Piece] = blokus.available_moves()
    print("nibot: ", len(avail_moves))
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




def s_bot(blokus: "Blokus") -> None:
    """
    Satisfactory bot. Chooses pieces using the function choose_larger, 
    where the bot prefers the play the largest piece it can play.

    Inputs: 
        blokus [Blokus]: the blokus game being played
    
    Returns [None]: Just plays or retires
    """
    avail_moves: set[Piece] = blokus.available_moves()
    print("sbot: ", len(avail_moves))
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

def u_bot(blokus: "Blokus") -> None:
    """
    Satisfactory bot. Chooses pieces using the function choose_larger, 
    where the bot prefers the play the largest piece it can play.

    Inputs: 
        blokus [Blokus]: the blokus game being played
    
    Returns [None]: Just plays or retires
    """
    avail_moves: set[Piece] = blokus.available_moves()
    print("Ubot: ", len(avail_moves))
    length = len(avail_moves)
    if length != 0:
        for _ in range(length):
            piece = choose_smaller(avail_moves)
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
    max_piece = pcs.pop()
    pcs.add(max_piece)
    for piece in pcs: 
        cur_len = len(piece.squares())
        if cur_len == 5:
            return piece
        if cur_len > max_squares:
            max_squares = cur_len
            max_piece = piece
        
    return max_piece

def choose_smaller(pcs: set[Piece]) -> Piece:
    min_squares: int = 0
    min_piece = pcs.pop()
    pcs.add(min_piece)
    for piece in pcs: 
        cur_len = len(piece.squares())
        if cur_len == 1:
            #i might add a cur_len < 4 line depending on how this performs
            return piece
        if cur_len < min_squares:
            min_squares = cur_len
            min_piece = piece
        
    return min_piece


@click.command()
@click.option('-n', '--num-games', type = click.INT, default = 20)
@click.option('-1', '--player1', type = click.STRING, default = "N")
@click.option('-2', '--player2', type = click.STRING, default = "N")

def main(player1: str, player2: str, num_games: int) -> str:
    win0 = 0
    win1 = 0
    tie = 0
    for _ in range(num_games):
        winners = game(player1, player2)
        if len(winners) > 1:
            tie += 1
        elif 1 in winners:
            win0 += 1
        else:
            win1 += 1
    return \
    f"Bot 0 Wins |  {(win0 / num_games) * 100} %\
    \nBot 1 Wins |  {(win1 / num_games) * 100} %\
    \nTies       |  {(tie / num_games) * 100} % \n"

print(main())