import pytest
from typing import Optional

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
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (1, 1)]

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
    assert shape.squares == [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, 0)]

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
    blokus = t_blokus_mini(1)
    shape = blokus.shapes[ShapeKind.Z]
    shape.flip_horizontally()
    assert shape.squares == [(-1, 1), (-1, 0), (0, 0), (1, 0), (1, -1)]

    shape = blokus.shapes[ShapeKind.W]
    shape.flip_horizontally()
    assert shape.squares == [(-1, -1), (0, -1), (0, 0), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.L]
    shape.flip_horizontally()
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, -1), (1, 0)]

def test_some_left_rotated_shapes() -> None:
    blokus = t_blokus_mini(1)
    shape = blokus.shapes[ShapeKind.Z]
    shape.rotate_left()
    assert shape.squares == [(-1, 1), (0, -1), (0, 0), (0, 1), (1, -1)]

    shape = blokus.shapes[ShapeKind.A]
    shape.rotate_left()
    assert shape.squares == [(-1, 0), (0, -1), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.V]
    shape.rotate_left()
    assert shape.squares == [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]

def test_some_right_rotated_shapes() -> None:
    blokus = t_blokus_mini(1)
    shape = blokus.shapes[ShapeKind.TWO]
    shape.rotate_right()
    assert shape.squares == [(0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.S]
    shape.rotate_right()
    assert shape.squares == [(-1, -1), (0, -1), (0, 0), (1, 0)]

    shape = blokus.shapes[ShapeKind.N]
    shape.rotate_right()
    assert shape.squares == [(0, -2), (0, -1), (0, 0), (1, 0), (1, 1)]
