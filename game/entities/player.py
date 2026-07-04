from dataclasses import dataclass

from game.board.position import Position


@dataclass
class Player:
    """
    Represents a player in the game.
    """

    name: str
    position: Position
    energy: int
    score: int = 0
