from copy import deepcopy
from dataclasses import dataclass

from game.board.board import Board
from game.entities.player import Player
from game.state.turn import Turn


@dataclass
class GameState:
    """
    Represents the complete state of an ongoing game.

    This class contains only data. All game logic should be
    implemented in the mechanics and controller modules.
    """

    board: Board
    player: Player
    ai: Player
    turn: Turn

    winner: Player | None = None
    game_over: bool = False

    difficulty: int = 2

    def clone(self) -> "GameState":
        """
        Returns a deep copy of the current game state.
        """
        return deepcopy(self)
