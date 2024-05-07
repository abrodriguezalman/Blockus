from typing import Optional

from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase

# Unoccupied grid cells are represented with None.
#
# Each occupied grid cell is represented as the player
# number whose piece occupies that square, plus the shape
# kind played there (ShapeKind.One, ShapeKind.W, etc).
#
# The shape kind is not needed to implement the game
# logic, but is exposed in case GUIs/TUIs would like
# to use the information in some way.
#
Cell = Optional[tuple[int, ShapeKind]]
Grid = list[list[Cell]]


class Blokus(BlokusBase):
    """
    Class for Blokus game.
    """


    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _retired_players: set[int]
    _start_positions: set[Point]
    _players: dict[int, dict[ShapeKind, Shape]]

    def __init__(self,
                 num_players: int,
                 size: int,
                 start_positions: set[Point]) -> None:
        """
        Attributes:
            num_players: Number of players
            size: Number of squares on each side of the board
            start_positions: Positions for players' first moves

        Raises ValueError (Not implemented yet)
            if num_players is less than 1 or more than 4,
            if the size is less than 5,
            if not all start_positions are on the board, or
            if there are fewer start_positions than num_players.
        """
        #check for ValueErrors, as specified in BlokusBase
        #for fake implementation, only support 1-2 players
        if num_players < 1 or num_players > 2:
            raise ValueError
        if size < 5:
            raise ValueError
        for x, y in start_positions:
            if x < 0 or y < 0 or x > size - 1 or y > size - 1:
                raise ValueError
        if len(start_positions) < num_players:
            raise ValueError

        #if no ValueErrors, proceed
        super().__init__(num_players, size, start_positions)
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._retired_players = set()

        #load in _shapes using the from_string method in piece.py
        self._shapes = {}
        for shape, rep in definitions.items():
            self._shapes[shape] = Shape.from_string(shape, rep)

        #a dictionary to keep track of the players and their pieces left
        #since this implementation only takes 2 players, this dictionary is
        #hardcoded to have two players. To be changed later
        self._players = {1: self._shapes.copy(), 2: self._shapes.copy()}

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        Returns all 21 Blokus shapes, as named and defined by
        the string representations in shape_definitions.py.

        The squares and origin, if any, of each shape should
        correspond to the locations and orientations defined
        in shape_definitions. For example, the five-square
        straight piece is called ShapeKind.FIVE, defined as a
        vertical line (as opposed to horizontal), and has its
        origin at the middle (third) square.

        See shape_definitions.py for more details.
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        Returns the board size (the number of squares per side).
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        Returns the start positions.
        """
        return self._start_positions

    @property
    def num_players(self) -> int:
        """
        Returns the number of players. Players are numbered
        consecutively, starting from 1.
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "Whose turn is it?"). While the
        game is ongoing, this property never refers to a player
        that has played all of their pieces or that retired
        before playing all of their pieces. If the game is over,
        this property will not return a meaningful value.
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        Returns the set of players who have retired. These
        players do not get any more turns; they are skipped
        over during subsequent gameplay.
        """
        return self._retired_players

    @property
    def grid(self) -> Grid:
        """
        Returns the current state of the board (i.e. Grid).
        There are two values tracked for each square (i.e. Cell)
        in the grid: the player number (an int) who has played
        a piece that occupies this square; and the shape kind
        of that piece. If no played piece occupies this square,
        then the Cell is None.
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        Returns whether or not the game is over. A game is over
        when every player is either retired or has played all
        their pieces.
        """
        #if all players are retired, return True
        if len(self.retired_players) == self.num_players:
            return True

        #if a player has not played all their pieces, return False
        for x in range(1, self.num_players + 1):
            if x not in self.retired_players:
                if len(self.remaining_shapes(x)) != 0:
                    return False
        return True

    @property
    def winners(self) -> Optional[list[int]]:
        """
        Returns the (one or more) players who have the highest
        score. Returns None if the game is not over.
        """
        if not self.game_over:
            return None

        win_list: list[int] = []
        max_score: int = -100000000
        for x in range(1, self.num_players+1):
            if self.get_score(x) > max_score:
                win_list = [x]
                max_score = self.get_score(x)
            elif self.get_score(x) == max_score:
                win_list.append(x)
        return win_list

    #
    # METHODS
    #

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        Returns a list of shape kinds that a particular
        player has not yet played.
        """
        return list(self._players[player].keys())

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall. For the purposes of this
        predicate, a "wall collision" occurs when at
        least one square of the piece would be located
        beyond the bounds of the (size x size) board.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None or not a valid position on the board.
        """
        #check ValueErrors
        piece._check_anchor()
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError

        #if the piece was placed at the given anchor, check for collisions
        for x, y in piece.squares():
            if x < 0 or y < 0 or x > self.size - 1 or y > self.size - 1:
                return True
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall or with any played pieces.
        A "collision" between pieces occurs when they
        overlap.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None or not a valid position on the board.
        """
        #check ValueErrors
        piece._check_anchor()
        assert not piece.anchor is None
        anchor_row, anchor_col = piece.anchor

        if anchor_row < 0 or anchor_col < 0 \
        or anchor_row > self.size - 1 or anchor_col > self.size - 1:
            raise ValueError
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError

        #check if the necessary grid space is empty
        for x, y in piece.squares():
            if self.grid[x][y] is not None:
                return True
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        If the current player has not already played
        this shape, this method returns a boolean
        indicating whether or not the given piece is
        legal to place. This requires that:

         - if the player has not yet played any pieces,
           this piece would cover a start position;
         - the piece would not collide with a wall or any
           previously played pieces; and
         - the piece shares one or more corners but no edges
           with the player's previously played pieces.

        Raises ValueError if the player has already
        played a piece with this shape.
        """
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError

        #for fake implementation, only check for collisions
        #don't need to check start position or corners-not-edges condition
        return not self.any_wall_collisions(piece) and not self.any_collisions(piece)


    def maybe_place(self, piece: Piece) -> bool:
        """
        If the piece is legal to place, this method
        places the piece on the board, updates the
        current player and other relevant game state,
        and returns True.

        If not, this method leaves the board and current
        game state unmodified, and returns False.

        Note that the game does not necessarily end right
        away when a player places their last piece; players
        who have not retired and have remaining pieces
        should still get their turns.

        Raises ValueError if the player has already
        played a piece with this shape.
        """
        #check if the piece is legal to place
        if self.legal_to_place(piece):

            #check if the piece we want to play is played before (or available
            #to play)
            if piece.shape.kind in self.remaining_shapes(self.curr_player):
                #remove the piece from remaining pieces
                del self._players[self.curr_player][piece.shape.kind]
            else:
                raise ValueError("This piece is already played")

            for square in piece.squares():
                x2, y2 = square
                #change the grid
                self._grid[x2][y2] = (self.curr_player, piece.shape.kind)

            #change who's turn it is - account for retired players
            self._curr_player = (self.curr_player % self.num_players) + 1
            if len(self.retired_players) != self.num_players:
                while self.curr_player in self.retired_players:
                    self._curr_player = (self.curr_player % self.num_players)+1

            return True

        return False

    def retire(self) -> None:
        """
        The current player, who has not played all their pieces,
        may choose to retire. This player does not get any more
        turns; they are skipped over during subsequent gameplay.
        """
        self._retired_players.add(self.curr_player)
        self._curr_player = (self.curr_player % self.num_players) + 1
        if len(self.retired_players) != self.num_players:
            while self.curr_player in self.retired_players:
                self._curr_player = (self.curr_player % self.num_players) + 1


    def get_score(self, player: int) -> int:
        """
        Returns the score for a given player. A player's score
        can be computed at any time during gameplay or at the
        completion of a game.
        """
        score: int = 0
        for shape in self._players[player].values():
            score += len(shape.squares)
        return -1 * score

    def available_moves(self) -> set[Piece]:
        """
        Returns the set of all possible moves that the current
        player may make. As with the arguments to the maybe_place
        method, a move is determined by a Piece, namely, one of
        the 21 Shapes plus a location and orientation.

        Notice there may be many different Pieces corresponding
        to a single Shape that are considered available moves
        (because they may differ in location and orientation).
        """
        raise NotImplementedError