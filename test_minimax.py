"""
Quick manual smoke test for the Minimax AI.
Run directly: python test_minimax.py

Not a pytest/unittest suite on purpose -- plays a few AI-vs-AI turns
at each difficulty depth and reports timing, so you can eyeball
correctness and confirm depth 6 is still fast enough to feel
responsive in the real game.
"""

import random
import time

from ai.minimax import select_best_move
from game.board.generator import BoardGenerator
from game.entities.player import Player
from game.rules import gameplay, victory
from game.rules.movement import get_valid_moves
from game.state.game_state import GameState
from game.state.turn import Turn

STARTING_ENERGY = 7


def _advance_turn(state: GameState) -> None:
    if victory.is_game_over(state):
        state.game_over = True
        state.winner = victory.get_winner(state)
        return
    state.turn = Turn.AI if state.turn == Turn.PLAYER else Turn.PLAYER


def new_state(difficulty: int) -> GameState:
    board, spawns = BoardGenerator.generate()
    player_spawn, ai_spawn = spawns
    return GameState(
        board=board,
        player=Player(name="Player", position=player_spawn, energy=STARTING_ENERGY),
        ai=Player(name="AI", position=ai_spawn, energy=STARTING_ENERGY),
        turn=Turn.AI,
        difficulty=difficulty,
    )


def play_random_player_turn(state: GameState) -> None:
    """Stand-in for the human player: picks a uniformly random legal move."""
    valid_moves = get_valid_moves(state.board, state.player.position)
    if state.player.energy < gameplay.MOVE_ENERGY_COST or not valid_moves:
        gameplay.skip_turn(state)
    else:
        gameplay.make_move(state, random.choice(valid_moves))
    _advance_turn(state)


def run_for_depth(depth: int, num_ai_moves: int = 4):
    state = new_state(depth)
    print(f"\n--- Depth {depth} ---")

    for i in range(num_ai_moves):
        if state.game_over:
            print(f"Game ended early after {i} AI moves. Winner: {state.winner}")
            return

        start = time.perf_counter()
        move = select_best_move(state, depth)
        elapsed = time.perf_counter() - start

        origin = state.ai.position
        if move is None:
            gameplay.skip_turn(state)
        else:
            gameplay.make_move(state, move)
        _advance_turn(state)

        print(
            f"Move {i}: AI {origin} -> {move} "
            f"(score={state.ai.score}, energy={state.ai.energy}) "
            f"took {elapsed:.3f}s"
        )

        if move is None:
            print("  AI had no legal move / no energy; skipped turn.")

        if state.game_over:
            print(f"Game ended after AI's move. Winner: {state.winner}")
            return

        play_random_player_turn(state)


def main():
    for depth in (2, 4, 6):
        run_for_depth(depth)


if __name__ == "__main__":
    main()
