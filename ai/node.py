from __future__ import annotations

from dataclasses import dataclass, field

from game.board.position import Position
from game.state.game_state import GameState


@dataclass
class Node:
    """
    A single node in the Minimax search tree.

    Wraps the game state reached by playing `move` (None for the
    root node), plus the children expanded from this state so far.
    """

    state: GameState
    move: Position | None = None
    children: list["Node"] = field(default_factory=list)
