import random
import click
from piece import Point, Piece
from blokus import Blokus

def game(player1: str, player2: str) -> list[int] | None:
    """
    The function that runs one game of blokus

    Inputs:
        player1 [str]: The strategy of the first player
        player2 [str]: The strategy of the second player

    Returns [list[int] | None]: returns a list showing who won, or None if
        the game is not over.
    """
    blokus = Blokus(2, 10, {(0,0), (9,9)})

    while not blokus.game_over:
        #player 1 (indexed as 0)
        choose_bot(player1, blokus)

        #player 2 (indexed as 1)
        choose_bot(player2, blokus)

    return blokus.winners


def rand_pos() -> Point:
    """
    Position randomizer, spits out a random point in a tuple
    """
    return (random.randint(1, 13), random.randint(1, 13))


def choose_bot(bot: str, blokus: "Blokus") -> None:
    """
    Turns the string representing the strategy of the bot to the actual bot. If
        there is no bot specified, ie the string is empty, then the default, 
        N-bot plays.
    
    Inputs:
        bot [str]: string representing the bot's strategy, S, N or U
        game ["Blokus"]: the blokus game that is currently being run

    Returns [None]
    """
    if bot == "S":
        s_bot(blokus)
    if bot == "N":
        ni_bot(blokus)
    if bot == "U":
        u_bot(blokus)
    if bot == "":
        ni_bot(blokus)

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
    if len(avail_moves) != 0:
        for _ in range(len(avail_moves)):
            piece = random.choice(list(avail_moves))
            if blokus.maybe_place(piece):
                return None
        blokus.retire()
        return None
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
    length = len(avail_moves)
    if length != 0:
        for _ in range(length):
            piece = choose_larger(avail_moves)
            if blokus.maybe_place(piece):
                return None
            avail_moves.remove(piece)
        blokus.retire()
        return None
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
    length = len(avail_moves)
    if length != 0:
        for _ in range(length):
            piece = choose_smaller(avail_moves)
            if blokus.maybe_place(piece):
                return None
            avail_moves.remove(piece)
        blokus.retire()
        return None
    blokus.retire()
    return None

def choose_larger(pcs: set[Piece]) -> Piece:
    """
    A function to choose the larger pieces out of a given set of pieces

    Inputs:
        pcs [set[Piece]]: the set of pieces to choose from

    Returns [Piece]: the comparatively large piece chosen. 
    """
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
    """
    A function to choose the smaller pieces out of a given set of pieces

    Inputs:
        pcs [set[Piece]]: the set of pieces to choose from

    Returns [Piece]: the comparatively small piece chosen. 
    """
    min_squares: int = 5
    min_piece = pcs.pop()
    pcs.add(min_piece)
    for piece in pcs:
        cur_len = len(piece.squares())
        if cur_len == 1:
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
    """
    The "main" loop that runs
    """
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

    print( \
    f"Bot 0 ({player1}) Wins |  {(win0 / num_games) * 100} %\
    \nBot 1 ({player2}) Wins |  {(win1 / num_games) * 100} %\
    \nTies           |  {(tie / num_games) * 100} % \n")

print(main())
