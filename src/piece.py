"""
Blokus shapes and pieces.

Modify only the methods marked as TODO.
"""
import copy
from typing import Optional
import textwrap
import numpy as np

from shape_definitions import ShapeKind

# A point is represented by row and column numbers (r, c). The
# top-left corner of a grid is (0, 0). Note that rows/columns
# correspond to vertical/horizontal axes, respectively. So, we
# will typically index into a 2-dimensional grid using
# grid[r][c] (as opposed to grid[y][x]).
#
Point = tuple[int, int]


# We will typically unpack a Point as follows: (r, c) = point
# In other cases, the row and col functions may be helpful.
#
def row(point: Point) -> int:
    return point[0]


def col(point: Point) -> int:
    return point[1]


class Shape:
    """
    Representing the 21 Blokus shapes, as named and defined by
    the string representations in shape_definitions.py.

    The locations of the squares are relative to the origin.

    The can_be_transformed boolean indicates whether or not
    the origin was explicitly defined in the string
    representation of the shape.

    See shape_definitions.py for more details.
    """

    kind: ShapeKind
    origin: Point
    can_be_transformed: bool
    squares: list[Point]

    def __init__(
        self,
        kind: ShapeKind,
        origin: Point,
        can_be_transformed: bool,
        squares: list[Point],
    ) -> None:
        """
        Constructor
        """
        self.kind = kind
        self.origin = origin
        self.can_be_transformed = can_be_transformed
        self.squares = squares

    def __str__(self) -> str:
        """
        Returns a complete string representation of the
        shape.
        """
        return f"""
            Shape
                kind = {self.kind}
                origin = {self.origin}
                can_be_transformed = {self.can_be_transformed}
                squares = {list(map(str, self.squares))}
        """

    @staticmethod
    def from_string(kind: ShapeKind, definition: str) -> "Shape":
        """
        Create a Shape based on its string representation
        in shape_definitions.py. See that file for details.
        """

        #defaults
        transform = False
        origin = (0,0)
        square = list()

        #split the string representation of the piece into rows
        #remove empty rows 
        rows = definition.split('\n')
        for row in rows:
            if not ('X' in row or 'O' in row or '@' in row):
                rows.remove(row)
        
        #strip away the extra units of leading whitespace 
        #all rows should now have the same length
        leading_space = min(len(row) - len(row.strip()) for row in rows)
        for i in range(len(rows)):
            if rows[i][0] == ' ':
                rows[i] = rows[i][leading_space:]

        #relative to (0,0) located in top left corner
        #locate origin, if one exists
        #and add points to square
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if rows[i][j] == 'O' or rows[i][j] == '@':
                    origin = (i, j)
                    transform = True
                if rows[i][j] != ' ' and rows[i][j] != '@':
                    square.append((i,j))
        
        #update points in square to be relative to origin
        for i in range(len(square)):
            square[i] = (square[i][0] - origin[0], square[i][1] - origin[1])     
            
        return Shape(kind, origin, transform, square)
        

    def flip_horizontally(self) -> None:
        """
        Flip the shape horizontally
        (across the vertical axis through its origin),
        by modifying the squares in place.
        """
        s = self.squares
        for i in range(len(s)):
            s[i] = (s[i][0], -s[i][1])

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        r = np.array(( (0, -1), (1, 0)))
        s = self.squares
        for i in range(len(s)):
            v = np.array((s[i][0], s[i][1]))
            s[i] = (r.dot(v)[0], r.dot(v)[1])

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        r = np.array(( (0, 1), (-1, 0)))
        s = self.squares
        for i in range(len(s)):
            v = np.array((s[i][0], s[i][1]))
            s[i] = (r.dot(v)[0], r.dot(v)[1])

class Piece:
    """
    A Piece takes a Shape and orients it on the board.

    The anchor point is used to locate the Shape.

    For flips and rotations, rather than storing these
    orientations directly (for example, using two attributes
    called face_up: bool and rotation: int), we modify
    the shape attribute in place. Therefore, it is important
    that each Piece object has its own deep copy of a
    Shape, so that transforming one Piece does not affect
    other Pieces that have the same Shape.
    """

    shape: Shape
    anchor: Optional[Point]

    def __init__(self, shape: Shape, face_up: bool = True, rotation: int = 0):
        """
        Each Piece will get its own deep copy of the given shape
        subject to initial transformations according to the arguments:

            face_up:  If true, the initial Shape will be flipped
                      horizontally.
            rotation: This number, modulo 4, indicates how many
                      times the shape should be right-rotated by
                      90 degrees.
        """
        # Deep copy shape, so that it can be transformed in place
        self.shape = copy.deepcopy(shape)

        # The anchor will be set by set_anchor
        self.anchor = None

        # We choose to flip...
        if not face_up:
            self.shape.flip_horizontally()

        # ... before rotating
        for _ in range(rotation % 4):
            self.shape.rotate_right()

    def set_anchor(self, anchor: Point) -> None:
        """
        Set the anchor point.
        """
        self.anchor = anchor

    def _check_anchor(self) -> None:
        """
        Raises ValueError if anchor is not set.
        Used by the flip and rotate methods below,
        so each of those may raise ValueError.
        """
        if self.anchor is None:
            raise ValueError(f"Piece does not have anchor: {self.shape}")

    def flip_horizontally(self) -> None:
        """
        Flip the piece horizontally.
        """
        self._check_anchor()
        self.shape.flip_horizontally()

    def rotate_left(self) -> None:
        """
        Rotate the shape left by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_left()

    def rotate_right(self) -> None:
        """
        Rotate the shape right by 90 degrees,
        by modifying the squares in place.
        """
        self._check_anchor()
        self.shape.rotate_right()

    def squares(self) -> list[Point]:
        """
        Returns the list of points corresponding to the
        current position and orientation of the piece.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        assert self.anchor is not None
        return [
            (row(self.anchor) + r, col(self.anchor) + c)
            for r, c in self.shape.squares
        ]
    

    def cardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined cardinal neighbors
        (north, south, east, and west)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()

        c_nghs = set()

        for sq in self.squares():
            x, y = sq
            if x > 0:
                c_nghs.add((x - 1, y))
            c_nghs.add((x + 1, y))
            if y > 0:
                c_nghs.add((x, y - 1))
            c_nghs.add((x, y + 1))

        for sq in self.squares():
            if sq in c_nghs:
                c_nghs.remove(sq)
    
        return c_nghs


    def intercardinal_neighbors(self) -> set[Point]:
        """
        Returns the combined intercardinal neighbors
        (northeast, southeast, southwest, and northwest)
        corresponding to all of the piece's squares.

        Raises ValueError if anchor is not set.
        """
        self._check_anchor()
        
        i_nghs = set()

        for sq in self.squares():
            x, y = sq
            if x > 0 and y > 0:
                i_nghs.add((x - 1, y - 1))
            if y > 0:
                i_nghs.add((x + 1, y - 1))
            i_nghs.add((x + 1, y + 1))
            if x > 0:
                i_nghs.add((x - 1, y + 1))

        for sq in self.squares():
            if sq in i_nghs:
                i_nghs.remove(sq)

        return i_nghs
    
