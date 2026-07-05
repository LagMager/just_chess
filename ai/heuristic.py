from game.board.position import Position
from game.rules.movement import get_valid_moves
from game.state.game_state import GameState

# Relative importance of each term. Score dominates because it is the
# actual win condition; the rest exist to give the search something
# useful to say about non-terminal states.
SCORE_WEIGHT = 10.0
ENERGY_WEIGHT = 1.0
MOBILITY_WEIGHT = 0.5
POTENTIAL_WEIGHT = 1.0


def _knight_distance_estimate(origin: Position, destination: Position) -> int:
    """
    Cheap stand-in for true knight-move distance (which needs a BFS
    per pair of squares). A knight covers roughly 3 rank+file steps
    per move, so this stays monotonic with the real distance without
    the search cost.
    """
    row_delta = abs(origin.row - destination.row)
    col_delta = abs(origin.column - destination.column)
    return max(1, (row_delta + col_delta + 1) // 3)


def _remaining_points_potential(state: GameState) -> float:
    """
    Rewards being closer than the opponent to each uncollected point
    tile. Score alone can't distinguish a promising position (near a
    big point tile) from a dead one, which matters at shallow depths
    where the search may never actually reach that tile.
    """
    board = state.board
    potential = 0.0
    for row in range(board.SIZE):
        for column in range(board.SIZE):
            tile = board.get_tile(Position(row, column))
            if not tile.points or tile.consumed:
                continue
            ai_distance = _knight_distance_estimate(state.ai.position, tile.position)
            player_distance = _knight_distance_estimate(
                state.player.position, tile.position
            )
            potential += tile.points * (1 / ai_distance - 1 / player_distance)
    return potential


def evaluate(state: GameState) -> float:
    """
    Scores `state` from the AI's point of view: positive favors the
    AI, negative favors the human player.
    """
    score_diff = state.ai.score - state.player.score
    energy_diff = state.ai.energy - state.player.energy
    mobility_diff = len(get_valid_moves(state.board, state.ai.position)) - len(
        get_valid_moves(state.board, state.player.position)
    )
    potential = _remaining_points_potential(state)

    return (
        SCORE_WEIGHT * score_diff
        + ENERGY_WEIGHT * energy_diff
        + MOBILITY_WEIGHT * mobility_diff
        + POTENTIAL_WEIGHT * potential
    )
