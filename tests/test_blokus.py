from typing import Optional
import pytest

import shape_definitions
from shape_definitions import ShapeKind
from piece import Shape, Piece
from base import BlokusBase
from blokus import Blokus

def test_inheritance() -> None:
    """Test that Blokus inherits from BlokusBase"""
    assert issubclass(Blokus,
                      BlokusBase), "BlokusFake should inherit from BlokusBase"

def t_blokus_mini(num_players: int) -> None:
    """Test the size, start_positions, num_players, curr_players, and grid have
    all been initialized correctly for Blokus Mini"""
    start_pos = {(0, 0), (0, 4), (4, 4), (4, 0), (2, 2)}
    size = 5
    b = Blokus(num_players, size, start_pos)
    assert b.size == size
    assert all(elem in b.start_positions for elem in start_pos)
    assert b.num_players == num_players
    assert b.curr_player == 1
    assert b.grid == [[None] * size for _ in range(size)]
    return b

def t_blokus_mono() -> None:
    """Test the size, start_positions, num_players, curr_players, and grid have
    all been initialized correctly for Blokus Mono"""
    start_pos = {(5, 5)}
    size = 11
    num_players = 1
    b = Blokus(num_players, size, start_pos)
    assert b.size == size
    assert all(elem in b.start_positions for elem in start_pos)
    assert b.num_players == num_players
    assert b.curr_player == 1
    assert b.grid == [[None] * size for _ in range(size)]
    return b

def t_blokus_duo() -> None:
    """Test the size, start_positions, num_players, curr_players, and grid have
    all been initialized correctly for Blokus Duo"""
    start_pos = {(4, 4), (9, 9)}
    size = 14
    num_players = 2
    b = Blokus(num_players, size, start_pos)
    assert b.size == size
    assert all(elem in b.start_positions for elem in start_pos)
    assert b.num_players == num_players
    assert b.curr_player == 1
    assert b.grid == [[None] * size for _ in range(size)]
    return b

def test_init_blokus_mini_1() -> None:
    """Test the size, start_positions, num_players, curr_players, and grid have
    all been initialized correctly for 1-player Blokus Mini"""
    t_blokus_mini(1)

def test_init_blokus_mini_2() -> None:
    """Test the size, start_positions, num_players, curr_players, and grid have
    all been initialized correctly for 2-player Blokus Mini"""
    t_blokus_mini(2)

def test_init_blokus_mono() -> None:
    """Test the size, start_positions, num_players, curr_players, and grid have
    all been initialized correctly for Blokus Mono"""
    t_blokus_mono()

def test_init_blokus_duo_2() -> None:
    """Test the size, start_positions, num_players, curr_players, and grid have
    all been initialized correctly for Blokus Duo"""
    t_blokus_duo()

def test_shapes_loaded() -> None:
    "Test that all shapes are loaded correctly"
    blokus = t_blokus_mini(1)
    # One piece shapes
    shape = blokus.shapes[ShapeKind.ONE]
    assert shape.kind == ShapeKind.ONE
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0)]

    # Two piece shapes
    shape = blokus.shapes[ShapeKind.TWO]
    assert shape.kind == ShapeKind.TWO
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1)]

    # Three piece shapes
    shape = blokus.shapes[ShapeKind.THREE]
    assert shape.kind == ShapeKind.THREE
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, -1), (0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.C]
    assert shape.kind == ShapeKind.C
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0)]

    # Four piece shapes
    shape = blokus.shapes[ShapeKind.FOUR]
    assert shape.kind == ShapeKind.FOUR
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, -1), (0, 0), (0, 1), (0, 2)]

    shape = blokus.shapes[ShapeKind.SEVEN]
    assert shape.kind == ShapeKind.SEVEN
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.S]
    assert shape.kind == ShapeKind.S
    assert shape.origin == (0, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, -1), (1, 0)]

    shape = blokus.shapes[ShapeKind.LETTER_O]
    assert shape.kind == ShapeKind.LETTER_O
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.A]
    assert shape.kind == ShapeKind.A
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (0, 1)]

    # Five piece blocks
    shape = blokus.shapes[ShapeKind.F]
    assert shape.kind == ShapeKind.F
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (-1, 1), (0, -1), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.FIVE]
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)]

    shape = blokus.shapes[ShapeKind.L]
    assert shape.kind == ShapeKind.L
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.N]
    assert shape.kind == ShapeKind.N
    assert shape.origin == (1, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 0), (0, 1), (1, 0), (2, 0)]

    shape = blokus.shapes[ShapeKind.P]
    assert shape.kind == ShapeKind.P
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1)]

    shape = blokus.shapes[ShapeKind.T]
    assert shape.kind == ShapeKind.T
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.U]
    assert shape.kind == ShapeKind.U
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 1), (0, -1), (0, 0), (0, 1)]

    shape = blokus.shapes[ShapeKind.V]
    assert shape.kind == ShapeKind.V
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.W]
    assert shape.kind == ShapeKind.W
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 0), (0, 1), (1, -1), (1, 0)]

    shape = blokus.shapes[ShapeKind.X]
    assert shape.kind == ShapeKind.X
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]

    shape = blokus.shapes[ShapeKind.Y]
    assert shape.kind == ShapeKind.Y
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (1, 0), (2, 0)]

    shape = blokus.shapes[ShapeKind.Z]
    assert shape.kind == ShapeKind.Z
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)]

def test_some_flipped_shapes() -> None:
    "Test that some shapes are flipped correctly"
    blokus = t_blokus_mini(1)
    shape = blokus.shapes[ShapeKind.Z]
    shape.flip_horizontally()
    assert shape.squares == [(-1, 1), (-1, 0), (0, 0), (1, 0), (1, -1)]

    shape = blokus.shapes[ShapeKind.W]
    shape.flip_horizontally()
    assert shape.squares == [(-1, -1), (0, 0), (0, -1), (1, 1), (1, 0)]

    shape = blokus.shapes[ShapeKind.L]
    shape.flip_horizontally()
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (1, -1)]

def test_some_left_rotated_shapes() -> None:
    "Test that some shapes can be left rotated correctly"
    blokus = t_blokus_mini(1)
    shape = blokus.shapes[ShapeKind.Z]
    shape.rotate_left()
    assert shape.squares == [(1, -1), (0, -1), (0, 0), (0, 1), (-1, 1)]

    shape = blokus.shapes[ShapeKind.A]
    shape.rotate_left()
    assert shape.squares == [(0, -1), (1, 0), (0, 0), (-1, 0)]

    shape = blokus.shapes[ShapeKind.V]
    shape.rotate_left()
    assert shape.squares == [(-1, -1), (-1, 0), (1, 1), (0, 1), (-1, 1)]

def test_some_right_rotated_shapes() -> None:
    "Test that some shapes can be right rotated correctly"
    blokus = t_blokus_mini(1)
    shape = blokus.shapes[ShapeKind.TWO]
    shape.rotate_right()
    assert shape.squares == [(0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.S]
    shape.rotate_right()
    assert shape.squares == [(0, 0), (1, 0), (-1, -1), (0, -1)]

    shape = blokus.shapes[ShapeKind.N]
    shape.rotate_right()
    assert shape.squares == [(1, 1), (0, 0), (1, 0), (0, -1), (0, -2)]

def test_some_cardinal_neighbors() -> None:
    """Test that the cardinal neighbors for some shapes can be determined
    correctly"""
    blokus = t_blokus_mono()

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    neighbors = piece_one.cardinal_neighbors()
    expected = {(0, 1), (1, 0)}
    assert all(elem in neighbors for elem in expected)

    piece_one = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_one.set_anchor((1, 1))
    neighbors = piece_one.cardinal_neighbors()
    expected = {(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2)}
    assert all(elem in neighbors for elem in expected)

    piece_one = Piece(blokus.shapes[ShapeKind.Y])
    piece_one.set_anchor((1, 1))
    neighbors = piece_one.cardinal_neighbors()
    expected = {(0, 0), (0, 2), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2), (4, 1)}
    assert all(elem in neighbors for elem in expected)

def test_some_intercardinal_neighbors() -> None:
    """Test that the intercardinal neighbors for some shapes can be determined
    correctly"""
    blokus = t_blokus_mono()

    piece_one = Piece(blokus.shapes[ShapeKind.TWO])
    piece_one.set_anchor((0, 0))
    neighbors = piece_one.intercardinal_neighbors()
    expected = {(1, 0), (1, 1), (1, 2)}
    assert all(elem in neighbors for elem in expected)

    piece_one = Piece(blokus.shapes[ShapeKind.C])
    piece_one.set_anchor((1, 1))
    neighbors = piece_one.intercardinal_neighbors()
    expected = {(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (2, 2), (2, 3),
                (3, 0), (3, 2)}
    assert all(elem in neighbors for elem in expected)

    piece_one = Piece(blokus.shapes[ShapeKind.F])
    piece_one.set_anchor((1, 1))
    neighbors = piece_one.intercardinal_neighbors()
    expected = {(0, 0), (1, 2), (1, 3), (2, 0), (2, 2), (3, 0), (3, 2)}
    assert all(elem in neighbors for elem in expected)

def test_one_player_blokus_mini_game() -> None:
    """Test that a one player blokus game can be created, and two moves can be
    done before retiring, and check game curr_player, maybe_place, and game_over
    values are correct at every step. Check get score and winner are correct
    after game over."""
    blokus = t_blokus_mini(1)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_one)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_two)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    piece_three = Piece(blokus.shapes[ShapeKind.C])
    piece_three.set_anchor((2, 3))
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_three)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    blokus.retire()

    assert blokus.game_over
    assert blokus.winners == [1]
    assert blokus.get_score(1) == -83

def test_two_player_blokus_mini_game() -> None:
    """Test that a two player blokus game can be created, and each player can
    make two moves before retiring, and check game curr_player, maybe_place, and
    game_over values are correct at every step. Check get score and winner are
    correct after game over."""
    blokus = t_blokus_mini(2)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_one)
    assert blokus.curr_player == 2
    assert not blokus.game_over

    piece_two = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two.set_anchor((4, 4))
    assert blokus.curr_player == 2
    assert blokus.maybe_place(piece_two)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    piece_three = Piece(blokus.shapes[ShapeKind.TWO])
    piece_three.set_anchor((1, 1))
    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_three)
    assert blokus.curr_player == 2
    assert not blokus.game_over

    piece_four = Piece(blokus.shapes[ShapeKind.TWO])
    piece_four.set_anchor((3, 2))
    assert blokus.curr_player == 2
    assert blokus.maybe_place(piece_four)
    assert blokus.curr_player == 1
    assert not blokus.game_over

    blokus.retire()
    assert blokus.curr_player == 2
    blokus.retire()

    assert blokus.game_over
    assert blokus.winners == [1, 2]
    assert blokus.get_score(1) == -86
    assert blokus.get_score(2) == -86

def test_exception_init() -> None:
    """Test that blokus constructor raises an error if there are fewer than 1
    player, if the size is less than 5, if the start pos is not on the board,
    and if there are fewer start pos than players"""
    with pytest.raises(ValueError):
        b = Blokus(0, 10, {(0, 0)})
    with pytest.raises(ValueError):
        b = Blokus(1, 2, {(0, 0)})
    with pytest.raises(ValueError):
        b = Blokus(1, 10, {(-1, 0)})
    with pytest.raises(ValueError):
        b = Blokus(2, 10, {(0, 0)})

def test_exception_place_already_played() -> None:
    """Test that if you try to place a piece twice it raises an error."""
    blokus = t_blokus_mini(1)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    piece_one.set_anchor((1, 0))
    with pytest.raises(ValueError):
        blokus.maybe_place(piece_one)

def test_exception_place_without_anchor() -> None:
    """Test that trying to place a piece without an anchor raises an error."""
    blokus = t_blokus_mini(1)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    with pytest.raises(ValueError):
        blokus.maybe_place(piece_one)

def t_place_first_pieces(blokus: Blokus) -> None:
    """Test that a piece must be played on a start position. Takes in a blokus
    board,a piece, and a bool which indicates whether this is the first piece"""
    # Can only place first piece on a start position
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 1))
    assert not blokus.maybe_place(piece_one)
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    # If there is a second player, make sure they can only place a piece
    # on a different start position.
    if blokus.num_players == 2:
        piece_two = Piece(blokus.shapes[ShapeKind.ONE])
        piece_two.set_anchor((1, 1))
        assert not blokus.maybe_place(piece_two)
        piece_two.set_anchor((0, 0))
        assert not blokus.maybe_place(piece_two)
        piece_two.set_anchor((13, 13))
        assert blokus.maybe_place(piece_two)

    # Place an additonal (two) piece(s)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)

    if blokus.num_players == 2:
        piece_four = Piece(blokus.shapes[ShapeKind.TWO])
        piece_four.set_anchor((12, 11))
        assert blokus.maybe_place(piece_four)

def test_start_positions_1() -> None:
    """Test that a piece must be played on the start position. Once the first
    piece is played on a start postition, the next piece can be played."""
    blokus = Blokus(1, 10, {(0, 0)})
    t_place_first_pieces(blokus)

def test_start_positions_2() -> None:
    """Test that each player must place their first piece on different start
    positions, and that each can play a piece afterward."""
    blokus = Blokus(2, 14, {(0, 0), (13, 13)})
    t_place_first_pieces(blokus)

def test_start_positions_3() -> None:
    """Same as previous, but with 4 start positions."""
    blokus = Blokus(2, 14, {(0, 0), (13, 0), (0, 13), (13, 13)})
    t_place_first_pieces(blokus)

def test_place_flipped_shape_1() -> None:
    """Test that a piece that is flipped once is placed correctly"""
    blokus = t_blokus_mini(1)
    piece = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece.set_anchor((2, 2))
    piece.flip_horizontally()
    assert piece.squares() == [(1, 3), (1, 2), (2, 2), (3, 2)]
    assert blokus.maybe_place(piece)

    for r in range(5):
        for c in range(5):
            if (r, c) in [(1, 3), (1, 2), (2, 2), (3, 2)]:
                assert blokus.grid[r][c] == (1, ShapeKind.SEVEN)
            else:
                assert blokus.grid[r][c] is None

def test_rotated_shape_1() -> None:
    """Test that a shape rotated right once is placed correctly"""
    blokus = t_blokus_mini(1)
    piece = Piece(blokus.shapes[ShapeKind.A])
    piece.set_anchor((2, 2))
    piece.rotate_right()
    assert piece.squares() == [(2, 3), (1, 2), (2, 2), (3, 2)]
    assert blokus.maybe_place(piece)

    for r in range(5):
        for c in range(5):
            if (r, c) in [(2, 3), (1, 2), (2, 2), (3, 2)]:
                assert blokus.grid[r][c] == (1, ShapeKind.A)
            else:
                assert blokus.grid[r][c] is None

def test_rotated_shape_2() -> None:
    """Test that a shape rotated right twice is placed correctly"""
    blokus = t_blokus_mini(1)
    piece = Piece(blokus.shapes[ShapeKind.A])
    piece.set_anchor((2, 2))
    piece.rotate_right()
    piece.rotate_right()
    assert piece.squares() == [(3, 2), (2, 3), (2, 2), (2, 1)]
    assert blokus.maybe_place(piece)

    for r in range(5):
        for c in range(5):
            if (r, c) in [(3, 2), (2, 3), (2, 2), (2, 1)]:
                assert blokus.grid[r][c] == (1, ShapeKind.A)
            else:
                assert blokus.grid[r][c] is None

def test_flipped_and_rotated_shape_1() -> None:
    """Test that a piece that is flipped and then right rotated three times
    is placed correctly"""
    blokus = t_blokus_mini(1)
    piece = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece.set_anchor((2, 2))
    piece.flip_horizontally()
    piece.rotate_right()
    piece.rotate_right()
    piece.rotate_right()
    assert piece.squares() == [(1, 1), (2, 1), (2, 2), (2, 3)]
    assert blokus.maybe_place(piece)

    for r in range(5):
        for c in range(5):
            if (r, c) in [(1, 1), (2, 1), (2, 2), (2, 3)]:
                assert blokus.grid[r][c] == (1, ShapeKind.SEVEN)
            else:
                assert blokus.grid[r][c] is None

def test_flipped_and_rotated_shape_2() -> None:
    """Test that a piece that is flipped twice and rotated four times is placed
    correctly"""
    blokus = t_blokus_mini(1)
    piece = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece.set_anchor((2, 2))
    piece.flip_horizontally()
    piece.flip_horizontally()
    piece.rotate_right()
    piece.rotate_right()
    piece.rotate_right()
    piece.rotate_right()
    assert piece.squares() == [(1, 1), (1, 2), (2, 2), (3, 2)]
    assert blokus.maybe_place(piece)

    for r in range(5):
        for c in range(5):
            if (r, c) in [(1, 1), (1, 2), (2, 2), (3, 2)]:
                assert blokus.grid[r][c] == (1, ShapeKind.SEVEN)
            else:
                assert blokus.grid[r][c] is None

def test_prevent_own_edges_1() -> None:
    """Test that you cannot play a piece that shares an edge with a previous
    piece"""
    blokus = t_blokus_mini(1)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((0, 1))
    assert not blokus.maybe_place(piece_two)

def test_prevent_own_edges_2() -> None:
    """Check that players can place pieces that share edges with other players'
    pieces but not their own"""
    blokus = t_blokus_duo()
    # Both players place a piece
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two.set_anchor((9, 9))
    assert blokus.maybe_place(piece_two)

    # Both players place another piece that does not touch edges with the first
    piece_three = Piece(blokus.shapes[ShapeKind.TWO])
    piece_three.set_anchor((4, 5))
    assert not blokus.maybe_place(piece_three)
    piece_three.set_anchor((5, 5))
    assert blokus.maybe_place(piece_three)

    piece_four = Piece(blokus.shapes[ShapeKind.TWO])
    piece_four.set_anchor((8, 9))
    assert not blokus.maybe_place(piece_four)
    piece_four.set_anchor((8, 8))
    assert blokus.maybe_place(piece_four)

    # Both players can place a piece that shares an edge with the other player's
    piece_five = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_five.set_anchor((6, 7))
    assert blokus.maybe_place(piece_three)

    piece_six = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_six.set_anchor((6, 5))
    assert blokus.maybe_place(piece_six)

def test_require_own_corners_1() -> None:
    """Test that a player must place a piece that shares a corner with a
    previously played one"""
    blokus = t_blokus_mini(1)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((2, 2))
    assert not blokus.maybe_place(piece_two)

def test_require_own_corners_2() -> None:
    """Test that players must play pieces that share corners with their own
    pieces but do not have to share corners with other players' pieces"""
    blokus = t_blokus_duo()
    # Both players place a piece
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((4, 4))
    assert blokus.maybe_place(piece_one)

    piece_two = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two.set_anchor((9, 9))
    assert blokus.maybe_place(piece_two)

    # Both players place another piece that shares a corner with the first
    piece_three = Piece(blokus.shapes[ShapeKind.TWO])
    piece_three.set_anchor((0, 0))
    assert not blokus.maybe_place(piece_three)
    piece_three.set_anchor((5, 5))
    assert blokus.maybe_place(piece_three)

    piece_four = Piece(blokus.shapes[ShapeKind.TWO])
    piece_four.set_anchor((12, 12))
    assert not blokus.maybe_place(piece_four)
    piece_four.set_anchor((8, 8))
    assert blokus.maybe_place(piece_four)

    # Both players can place a piece that doesn't share a corner with the other
    # player's
    piece_five = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_five.set_anchor((3, 7))
    assert blokus.maybe_place(piece_three)

    piece_six = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_six.set_anchor((9, 5))
    assert blokus.maybe_place(piece_six)

def test_some_available_moves() -> None:
    """Verify available_moves is non-empty, and that it decreases in size after
    some pieces have been played"""
    blokus = t_blokus_mini(1)
    n = blokus.available_moves()
    assert n != 0

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)

    assert n > blokus.available_moves()

def test_no_available_moves() -> None:
    """Test that available_moves is empty after playing all pieces"""

