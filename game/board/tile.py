from dataclasses import dataclass

from game.board.position import Position


@dataclass
class Tile:
    """
    Represents a single square on the board.

    Attributes:
        position: Coordinates of the tile.
        points: Score awarded when this tile is collected.
        energy: Energy restored when this tile is collected.
        consumed: Whether the tile has already been used.
    """

    position: Position
    points: int = 0
    energy: int = 0
    consumed: bool = False
