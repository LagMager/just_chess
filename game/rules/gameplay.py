from game.board.position import Position
from game.state.game_state import GameState
from game.state.turn import Turn

MOVE_ENERGY_COST = 1
SKIP_TURN_PENALTY = 3


def _current_player(game_state: GameState):
    """
    Returns whichever player (human or AI) is acting this turn.
    """
    return game_state.player if game_state.turn == Turn.PLAYER else game_state.ai


def apply_move(game_state: GameState, destination: Position) -> None:
    """
    Applies a legal move to the current player.
    """
    player = _current_player(game_state)
    player.position = destination


def consume_energy(game_state: GameState, amount: int) -> None:
    """
    Consumes energy from the current player.
    """
    player = _current_player(game_state)
    player.energy -= amount


def recover_energy(game_state: GameState, amount: int) -> None:
    """
    Restores energy to the current player.
    """
    player = _current_player(game_state)
    player.energy += amount


def collect_points(game_state: GameState, points: int) -> None:
    """
    Adds points to the current player.
    """
    player = _current_player(game_state)
    player.score += points


def consume_tile(game_state: GameState, destination: Position) -> None:
    """
    Marks the destination tile as consumed.
    """
    game_state.board.consume_tile(destination)


def resolve_tile(game_state: GameState, destination: Position) -> None:
    """
    Applies the effect of landing on a tile: awards points or energy
    if the tile hasn't been consumed yet, then consumes it.
    """
    tile = game_state.board.get_tile(destination)
    if tile.consumed:
        return

    if tile.points:
        collect_points(game_state, tile.points)
    if tile.energy:
        recover_energy(game_state, tile.energy)

    consume_tile(game_state, destination)


def make_move(game_state: GameState, destination: Position) -> None:
    """
    Performs a full move: pays the energy cost, relocates the
    current player, and resolves any tile effects at the destination.
    """
    consume_energy(game_state, MOVE_ENERGY_COST)
    apply_move(game_state, destination)
    resolve_tile(game_state, destination)


def skip_turn(game_state: GameState) -> None:
    """
    Applies the penalty for a player who cannot move: a 3 point
    deduction, no other state change.
    """
    player = _current_player(game_state)
    player.score -= SKIP_TURN_PENALTY
