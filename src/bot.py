from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase
from blokus import Blokus
from fakes import BlokusStub

import sys
import random
from typing import Optional

times = int(sys.argv[1])

#position randomizer
def rand_pos():
    return (random.randint(1, 13), random.randint(1, 13))

def game():
    stub_bot = BlokusStub(2, 14, {rand_pos(), rand_pos()})
    while not stub_bot.game_over:
        piece = ni_bot(stub_bot)
        stub_bot.maybe_place(piece)

    return stub_bot.winners

def ni_bot(stub: "BlokusStub"):
    """
    The needs improvement bot. This bot decides which piece to play and where
    on completely random.

    Inputs:
        stub [BlokusStub]: the stub implementation of blokus that is currently 
            running

    Returns: 
        [Piece] if it can play
        [None] if there are no available moves left
    
    """
    if len(stub.available_moves()) != 0:
        piece = random.choice(list(stub.available_moves()))
        return piece
    return None

def main():
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





