from game.board.generator import BoardGenerator
from game.board.position import Position
from game.entities.player import Player
from game.rules import gameplay, victory
from game.rules.movement import is_valid_move
from game.state.game_state import GameState
from game.state.turn import Turn

STARTING_ENERGY = 7


class GameController:
    """
    Orchestrates a full game: setup, move handling, turn switching,
    and end-of-game detection. Delegates actual rule logic to the
    gameplay and victory modules.
    """

    def __init__(self) -> None:
        self._game_state: GameState | None = None

    def new_game(self, difficulty: int = 2) -> GameState:
        """
        Starts a new game with a freshly generated board and two
        players at random, safe (non-point, non-energy) positions.
        The machine always makes the first move.
        """
        board, spawn_positions = BoardGenerator.generate()
        player_spawn, ai_spawn = spawn_positions

        player = Player(name="Player", position=player_spawn, energy=STARTING_ENERGY)
        ai = Player(name="AI", position=ai_spawn, energy=STARTING_ENERGY)

        self._game_state = GameState(
            board=board,
            player=player,
            ai=ai,
            turn=Turn.AI,
            difficulty=difficulty,
        )
        return self._game_state

    def make_move(self, destination: Position) -> None:
        """
        Attempts to move the current player to the given destination.
        Handles energy costs, tile effects, skipped turns, turn
        switching, and end-of-game detection.
        """
        game_state = self._require_game_state()

        if game_state.game_over:
            return

        current_player = self._current_player()

        if current_player.energy < gameplay.MOVE_ENERGY_COST:
            gameplay.skip_turn(game_state)
        elif is_valid_move(game_state.board, current_player.position, destination):
            gameplay.make_move(game_state, destination)
        else:
            return  # illegal move; UI is responsible for only offering valid ones

        self._finish_turn()

    def get_game_state(self) -> GameState:
        """
        Returns the current game state.
        """
        return self._require_game_state()

    def _current_player(self) -> Player:
        game_state = self._require_game_state()
        return game_state.player if game_state.turn == Turn.PLAYER else game_state.ai

    def _finish_turn(self) -> None:
        game_state = self._require_game_state()

        if victory.is_game_over(game_state):
            game_state.game_over = True
            game_state.winner = victory.get_winner(game_state)
            return

        game_state.turn = Turn.AI if game_state.turn == Turn.PLAYER else Turn.PLAYER

    def _require_game_state(self) -> GameState:
        if self._game_state is None:
            raise RuntimeError("No active game. Call new_game() first.")
        return self._game_state
