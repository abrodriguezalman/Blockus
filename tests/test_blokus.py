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

def t_blokus_mini(num_players: int) -> Blokus:
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

def t_blokus_mono() -> Blokus:
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

def t_blokus_duo() -> Blokus:
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

    shapes = {ShapeKind.ONE: [(0, 0), [(0, 0)]],
              ShapeKind.TWO: [(0, 0), [(0, 0), (0, 1)]],
              ShapeKind.THREE: [(0, 1), [(0, -1), (0, 0), (0, 1)]],
              ShapeKind.C: [(0, 0), [(0, 0), (0, 1), (1, 0)]],
              ShapeKind.FOUR: [(0, 1), [(0, -1), (0, 0), (0, 1), (0, 2)]],
              ShapeKind.SEVEN: [(1, 1), [(-1, -1), (-1, 0), (0, 0), (1, 0)]],
              ShapeKind.S: [(0, 1), [(0, 0), (0, 1), (1, -1), (1, 0)]],
              ShapeKind.LETTER_O: [(0, 0), [(0, 0), (0, 1), (1, 0), (1, 1)]],
              ShapeKind.A: [(1, 1), [(-1, 0), (0, -1), (0, 0), (0, 1)]],
              ShapeKind.F: [(1, 1),
                            [(-1, 0), (-1, 1), (0, -1), (0, 0), (1, 0)]],
              ShapeKind.FIVE: [(2, 0),
                               [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)]],
              ShapeKind.L: [(2, 0),
                            [(-2, 0), (-1, 0), (0, 0), (1, 0), (1, 1)]],
              ShapeKind.N: [(1, 0),
                            [(-1, 1), (0, 0), (0, 1), (1, 0), (2, 0)]],
              ShapeKind.P: [(1, 1),
                            [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1)]],
              ShapeKind.T: [(1, 1),
                            [(-1, -1), (-1, 0), (-1, 1), (0, 0), (1, 0)]],
              ShapeKind.U: [(1, 1),
                            [(-1, -1), (-1, 1), (0, -1), (0, 0), (0, 1)]],
              ShapeKind.V: [(1, 1),
                            [(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]],
              ShapeKind.W: [(1, 1),
                            [(-1, 1), (0, 0), (0, 1), (1, -1), (1, 0)]],
              ShapeKind.X: [(1, 1),
                            [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]],
              ShapeKind.Y: [(1, 1),
                            [(-1, 0), (0, -1), (0, 0), (1, 0), (2, 0)]],
              ShapeKind.Z: [(1, 1),
                            [(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)]]
              }
    for shape_kind, points in shapes.items():
        shape = blokus.shapes[shape_kind]
        assert shape.kind == shape_kind
        assert shape.origin == points[0]
        if shape_kind in (ShapeKind.ONE, ShapeKind.LETTER_O):
            assert not shape.can_be_transformed
        else:
            assert shape.can_be_transformed
        assert shape.squares == points[1]

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
        Blokus(0, 10, {(0, 0)})
    with pytest.raises(ValueError):
        Blokus(1, 2, {(0, 0)})
    with pytest.raises(ValueError):
        Blokus(1, 10, {(-1, 0)})
    with pytest.raises(ValueError):
        Blokus(2, 10, {(0, 0)})

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
    piece_four.set_anchor((8, 7))
    assert blokus.maybe_place(piece_four)

    # Both players can place a piece that shares an edge with the other player's
    piece_five = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_five.set_anchor((6, 7))
    assert blokus.maybe_place(piece_five)

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
    piece_four.set_anchor((8, 7))
    assert blokus.maybe_place(piece_four)

    # Both players can place a piece that doesn't share a corner with the other
    # player's
    piece_five = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_five.set_anchor((3, 7))
    assert blokus.maybe_place(piece_five)

    piece_six = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece_six.set_anchor((9, 5))
    assert blokus.maybe_place(piece_six)

def test_some_available_moves() -> None:
    """Verify available_moves is non-empty, and that it decreases in size after
    some pieces have been played"""
    blokus = t_blokus_mini(1)
    n = len(blokus.available_moves())
    assert n != 0

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((1, 1))
    assert blokus.maybe_place(piece_two)

    assert n > len(blokus.available_moves())

def test_no_available_moves() -> None:
    """Test that available_moves is empty after playing all pieces"""
    blokus = Blokus(1, 5, {(0, 0)})

    piece_one = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_one.set_anchor((2, 0))
    assert blokus.maybe_place(piece_one)

    assert len(blokus.available_moves()) == 0

def place_most_pieces(blokus: Blokus) -> None:
    """Place all but the last two pieces on a board. Helper for next two
    tests."""
    def place_piece(
        kind: ShapeKind, row: int, col: int
    ) -> None:
        assert blokus.curr_player == 1
        assert not blokus.game_over

        piece = Piece(blokus.shapes[kind])

        # Place the piece in the specified location
        piece.set_anchor((row, col))
        assert blokus.maybe_place(piece)

    place_piece(ShapeKind.Z, 1, 1)
    place_piece(ShapeKind.Y, 1, 4)
    place_piece(ShapeKind.X, 5, 3)
    place_piece(ShapeKind.W, 3, 6)
    place_piece(ShapeKind.V, 3, 9)
    place_piece(ShapeKind.U, 8, 1)
    place_piece(ShapeKind.T, 2, 12)
    place_piece(ShapeKind.P, 7, 6)
    place_piece(ShapeKind.LETTER_O, 0, 8)
    place_piece(ShapeKind.N, 4, 13)
    place_piece(ShapeKind.L, 7, 11)
    place_piece(ShapeKind.F, 8, 8)
    place_piece(ShapeKind.SEVEN, 11, 10)
    place_piece(ShapeKind.FIVE, 11, 3)
    place_piece(ShapeKind.A, 14, 1)
    place_piece(ShapeKind.FOUR, 13, 12)
    place_piece(ShapeKind.THREE, 14, 5)
    place_piece(ShapeKind.C, 12, 7)
    place_piece(ShapeKind.S, 14, 8)


def test_15_points() -> None:
    """Test that when all pieces are played, a player scores 15 points."""
    blokus = Blokus(1, 16, {(0, 0)})
    place_most_pieces(blokus)

    # After placing the other pieces, play the one piece then the two piece
    assert blokus.curr_player == 1
    assert not blokus.game_over
    piece = Piece(blokus.shapes[ShapeKind.ONE])
    piece.set_anchor((4, 1))
    assert blokus.maybe_place(piece)

    assert blokus.curr_player == 1
    assert not blokus.game_over
    piece = Piece(blokus.shapes[ShapeKind.TWO])
    piece.set_anchor((0, 14))
    assert blokus.maybe_place(piece)

    assert blokus.game_over
    assert blokus.get_score(1) == 15
    assert blokus.winners == [1]

def test_20_points() -> None:
    """Test when a player places all pieces and the 1-piece is played last, they
    earn 20 points"""
    blokus = Blokus(1, 16, {(0, 0)})
    place_most_pieces(blokus)

    # After placing the other pieces, play the one piece then the two piece
    assert blokus.curr_player == 1
    assert not blokus.game_over
    piece = Piece(blokus.shapes[ShapeKind.TWO])
    piece.set_anchor((0, 14))
    assert blokus.maybe_place(piece)

    assert blokus.curr_player == 1
    assert not blokus.game_over
    piece = Piece(blokus.shapes[ShapeKind.ONE])
    piece.set_anchor((4, 1))
    assert blokus.maybe_place(piece)

    assert blokus.game_over
    assert blokus.get_score(1) == 20
    assert blokus.winners == [1]
