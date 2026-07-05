from game.board.board import Board
from game.board.position import Position
from game.entities.player import Player
from game.rules.movement import get_valid_moves
from game.state.game_state import GameState


def has_available_moves(board: Board, player: Player) -> bool:
    """
    Returns whether the player has enough energy and at least
    one legal knight move from their current position.
    """
    if player.energy <= 0:
        return False
    return len(get_valid_moves(board, player.position)) > 0


def has_remaining_points(board: Board) -> bool:
    """
    Returns whether any unconsumed point tile remains on the board.
    """
    for row in range(board.SIZE):
        for column in range(board.SIZE):
            tile = board.get_tile(Position(row, column))
            if tile.points and not tile.consumed:
                return True
    return False


def is_game_over(game_state: GameState) -> bool:
    """
    Returns whether the game has ended: no point tiles remain,
    or neither player can make a move.
    """
    board = game_state.board
    if not has_remaining_points(board):
        return True

    player_can_move = has_available_moves(board, game_state.player)
    ai_can_move = has_available_moves(board, game_state.ai)
    return not player_can_move and not ai_can_move


def get_winner(game_state: GameState) -> Player | None:
    """
    Returns the player with the highest score, or None if tied.
    """
    if game_state.player.score > game_state.ai.score:
        return game_state.player
    if game_state.ai.score > game_state.player.score:
        return game_state.ai
    return None
