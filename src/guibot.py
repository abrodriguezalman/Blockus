from shape_definitions import ShapeKind
from fakes import BlokusFake
from piece import Point, Shape, Piece
from base import BlokusBase, Grid
from blokus import Blokus

import sys
import random
from typing import Optional

#times = int(sys.argv[1])

class NIBot():

    def __init__(self):
        pass

    def ni_bot(self, blokus: "BlokusBase", avail_moves: set[Piece]) -> Piece:
        """
        The needs improvement bot. This bot decides which piece to play and where
        on completely random.

        Inputs:
            blokus [BlokusFake]: the fake implementation of blokus that is currently 
                running

        Returns: [None], just plays or retires
        
        """
        #avail_moves: set[Piece] = blokus.available_moves()

        print(len(avail_moves))
        if len(avail_moves) != 0:
            for _ in range(len(avail_moves)):
                piece: Piece = avail_moves.pop()
            
                if blokus.legal_to_place(piece):
                    
                    print("bot played a piece")
                    return piece
                    #return None
            #print("1: retiring")
            #blokus.retire()
            #return None
        else:
            print("1: retiring")
            blokus.retire()
    
        return "I played"
    
    #position randomizer
    def rand_pos() -> Point:
        return (random.randint(1, 13), random.randint(1, 13))

    """def game() -> list[int]:
        game = BlokusFake(2, 6, {(0,0), (5,5)})
    
        while not game.game_over:
            print("bot1 starts playing")
            ni_bot(game)
            print("bot1 played")
            print("bot2 starts playing")
            ni_bot(game)
            print("bot2 played")
    
        print(game.grid)
        return game.winners"""

            
        
    

"""def s_bot(blokus: "BlokusFake"):
    avail_moves = list(blokus.available_moves())
    return 


def main(times: int = 4):
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

print(main())"""

