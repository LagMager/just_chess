from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Position:
    """
    Represents a position on the chess board.
    """

    row: int
    column: int
