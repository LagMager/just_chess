from dataclasses import dataclass

from game.board.position import Position


@dataclass(frozen=True)
class Move:
    """
    Represents a move from one position to another.
    """

    origin: Position
    destination: Position
