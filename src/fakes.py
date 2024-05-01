"""
Fake implementations of BlokusBase.

We provide a BlokusStub implementation, and
you must provide a BlokusFake implementation.
"""
from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid
from typing import Optional

class BlokusStub(BlokusBase):
    """
    Stub implementation of BlokusBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players.
    - Only three of the 21 Blokus shapes are available:
      the one-square, two-square, and three-square straight pieces.
    - Players are allowed to place pieces in any position of the board
      they want, even if the piece collides with any squares of
      previously played pieces (squares of the new piece replace any
      conflicting ones).
    - Board positions are not validated. If a method is called with
      a position outside the board, it will likely cause an exception.
    - There is no consideration of start positions for a player's
      first move.
    - The constructor simulates two initial moves: placing
      Player 1's "1" piece in the top-left corner and
      Player 2's "2" piece in the bottom-right corner.
    - The game ends after six moves. The player, if any, who has a
      piece occupying the top-right corner of the board wins.
      Otherwise, the players tie.
    - The `remaining_shapes` method always says all three shapes remain.
    - The only shape that is considered available by `available_moves`
      is the one-square shape, and it is considered available everywhere
      on the board regardless of whether the corresponding positions are
      available or occupied.
    - Several methods return simple, unhelpful results (as opposed to
      raising NotImplementedErrors).
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Constructor (See BlokusBase)

        This stub initializes a counter for number of moves
        in order to implement a simple game_over condition.

        Once everything is initialized, this stub implementation
        "simulates" two moves.
        """
        super().__init__(num_players, size, start_positions)
        self._shapes = self._load_shapes()
        self._size = size
        self._num_players = 2
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._num_moves = 0
        self._simulate_two_moves()

    def _load_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Rather than reading in the representations of shapes
        from shape_definitions.py, this method manually builds
        three of the 21 kinds of shapes.

        See shape_definitions.py for more details.
        """
        # See shape_definitions.definitions[ShapeKind.ONE]
        shape_1 = Shape(ShapeKind.ONE, (0, 0), False, [(0, 0)])

        # See shape_definitions.definitions[ShapeKind.TWO]
        shape_2 = Shape(ShapeKind.TWO, (0, 0), True, [(0, 0), (0, 1)])

        # See shape_definitions.definitions[ShapeKind.THREE]
        shape_3 = Shape(
            ShapeKind.THREE, (0, 1), True, [(0, -1), (0, 0), (0, 1)]
        )

        return {
            ShapeKind.ONE: shape_1,
            ShapeKind.TWO: shape_2,
            ShapeKind.THREE: shape_3,
        }

    def _simulate_two_moves(self) -> None:
        """
        Simulates two moves:

        - Player 1 places their ShapeKind.ONE piece in the top-left corner.
        - Player 2 places their ShapeKind.TWO piece in the bottom-right corner.

        This drives the game into a state where four more pieces
        can be played before entering the game_over condition
        (six moves total).
        """
        piece_1 = Piece(self.shapes[ShapeKind.ONE])
        piece_1.set_anchor((0, 0))
        self.maybe_place(piece_1)

        # This anchor position accounts for the origin of
        # ShapeKind.TWO as specified in shape_definitions.py.
        piece_2 = Piece(self.shapes[ShapeKind.TWO])
        piece_2.set_anchor((self.size - 1, self.size - 2))
        self.maybe_place(piece_2)

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        return set()

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return set()

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        return self._num_moves == 6

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase
        """
        top_right_cell = self.grid[0][self.size - 1]
        if top_right_cell is None:
            return [1, 2]
        else:
            winner = top_right_cell[0]
            return [winner]

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase
        """
        return [ShapeKind.ONE, ShapeKind.TWO, ShapeKind.THREE]

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return True

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        for r, c in piece.squares():
            self._grid[r][c] = (self.curr_player, piece.shape.kind)
        self._curr_player = (self.curr_player % self.num_players) + 1
        self._num_moves += 1
        return True

    def retire(self) -> None:
        """
        See BlokusBase
        """
        pass

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        return -999

    def available_moves(self) -> set[Piece]:
        """
        See BlokusBase
        """
        pieces = set()
        for r in range(self.size):
            for c in range(self.size):
                piece = Piece(self.shapes[ShapeKind.ONE])
                piece.set_anchor((r, c))
                pieces.add(piece)

        return pieces


#
# Your BlokusFake implementation goes here
#
class BlokusFake(BlokusBase):
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
        
        #check for ValueErrors, as specified in BlokusBase
        #for fake implementation, only support 1-2 players
        if num_players < 1 or num_players > 2:
            raise ValueError
        if size < 5:
            raise ValueError
        for x, y in start_positions:
            if x < 0 or y < 0 or x > size-1 or y > size-1:
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
        for shape in definitions:
            self._shapes[shape] = Shape.from_string(shape, definitions[shape])

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
        
        win_list = list()
        max_score = -100000000
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
            if x < 0 or y < 0 or x > self.size-1 or y > self.size-1:
                return False
            
        return True

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
        if piece.anchor[0] < 0 or piece.anchor[1] < 0 \
            or piece.anchor[0] > self.size-1 or piece.anchor[1] > self.size-1:
                raise ValueError
        if piece.shape.kind not in self.remaining_shapes(self.curr_player):
            raise ValueError
        
        #check if the necessary grid space is empty
        for x, y in piece.squares():
            if self.grid[x][y] is not None:
                return False
        return True
        

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
        return self.any_wall_collisions(piece) and self.any_collisions(piece)

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
                raise ValueError(f"This piece is already played")

            for square in piece.squares(): 
                x2, y2 = square
                #change the grid
                self._grid[x2][y2] = (self.curr_player, piece.shape.kind)
            
            #change who's turn it is - account for retired players
            self._curr_player = (self.curr_player % self.num_players) + 1
            while self.curr_player in self.retired_players:
                self._curr_player = (self.curr_player % self.num_players) + 1

            return True

        return False


    def retire(self) -> None:
        """
        The current player, who has not played all their pieces,
        may choose to retire. This player does not get any more
        turns; they are skipped over during subsequent gameplay.
        """
        self._retired_players.add(self.curr_player)

    def get_score(self, player: int) -> int:
        """
        Returns the score for a given player. A player's score
        can be computed at any time during gameplay or at the
        completion of a game.
        """
        score = 0
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
