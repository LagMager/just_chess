from game.board.board import Board
from game.board.position import Position
from game.board.tile import Tile
from game.entities.player import Player
from game.rules import gameplay, victory
from game.rules.movement import get_valid_moves
from game.state.game_state import GameState
from game.state.turn import Turn

from ai.heuristic import evaluate
from ai.node import Node


def _current_player(state: GameState):
    return state.player if state.turn == Turn.PLAYER else state.ai


def _clone_board(board: Board) -> Board:
    """
    Rebuilds a board via the public Tile API instead of GameState's
    deepcopy. deepcopy's generic reflection makes it the dominant
    cost of a Minimax node (hundreds of thousands of clones at depth
    6); this is a direct field copy instead.
    """
    clone = Board()
    for row in range(board.SIZE):
        for column in range(board.SIZE):
            tile = board.get_tile(Position(row, column))
            if tile.points or tile.energy or tile.consumed:
                clone.set_tile(
                    Tile(
                        position=tile.position,
                        points=tile.points,
                        energy=tile.energy,
                        consumed=tile.consumed,
                    )
                )
    return clone


def _clone_state(state: GameState) -> GameState:
    """Fast alternative to GameState.clone() for the Minimax hot path."""
    return GameState(
        board=_clone_board(state.board),
        player=Player(
            name=state.player.name,
            position=state.player.position,
            energy=state.player.energy,
            score=state.player.score,
        ),
        ai=Player(
            name=state.ai.name,
            position=state.ai.position,
            energy=state.ai.energy,
            score=state.ai.score,
        ),
        turn=state.turn,
        winner=state.winner,
        game_over=state.game_over,
        difficulty=state.difficulty,
    )


def _advance_turn(state: GameState) -> None:
    """
    Mirrors GameController._finish_turn: check for game end, then
    hand the turn to the other player. Duplicated here (instead of
    reused from the controller) so the AI module only depends on the
    pure rule functions, not on the stateful controller.
    """
    if victory.is_game_over(state):
        state.game_over = True
        state.winner = victory.get_winner(state)
        return
    state.turn = Turn.AI if state.turn == Turn.PLAYER else Turn.PLAYER


def generate_children(node: Node) -> list[Node]:
    """
    Expands `node` one ply: one child per legal knight move of
    whoever's turn it is in `node.state`, or a single skip-turn child
    if that player has no energy or no legal move.
    """
    state = node.state
    if state.game_over:
        node.children = []
        return node.children

    current_player = _current_player(state)
    valid_moves = get_valid_moves(state.board, current_player.position)

    if current_player.energy < gameplay.MOVE_ENERGY_COST or not valid_moves:
        child_state = _clone_state(state)
        gameplay.skip_turn(child_state)
        _advance_turn(child_state)
        node.children = [Node(state=child_state, move=None)]
        return node.children

    children = []
    for destination in valid_moves:
        child_state = _clone_state(state)
        gameplay.make_move(child_state, destination)
        _advance_turn(child_state)
        children.append(Node(state=child_state, move=destination))

    node.children = children
    return children


def minimax(
    node: Node,
    depth: int,
    alpha: float = float("-inf"),
    beta: float = float("inf"),
) -> float:
    """
    Depth-limited minimax with a heuristic cutoff and alpha-beta
    pruning. Whoever's turn it is at `node.state` picks among its
    children: the AI maximizes, the human player minimizes. Pruning
    only skips branches that provably can't change that choice, so
    the returned value is identical to plain minimax -- just faster,
    which is what makes depth 6 practical to run on every AI turn.
    """
    state = node.state
    if depth == 0 or state.game_over:
        return evaluate(state)

    children = generate_children(node)
    if not children:
        return evaluate(state)

    maximizing = state.turn == Turn.AI
    # Trying the most promising move first (per the heuristic) lets
    # alpha-beta cut off the rest of the sibling list far more often.
    children.sort(key=lambda child: evaluate(child.state), reverse=maximizing)

    if maximizing:
        value = float("-inf")
        for child in children:
            value = max(value, minimax(child, depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    value = float("inf")
    for child in children:
        value = min(value, minimax(child, depth - 1, alpha, beta))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def select_best_move(state: GameState, depth: int) -> Position | None:
    """
    Returns the destination the AI should move to from `state`
    (assumed to be the AI's turn), or None if it must skip its turn.
    `depth` is the number of plies to look ahead, taken directly from
    the selected difficulty (2 / 4 / 6).
    """
    root = Node(state=state)
    children = generate_children(root)

    if len(children) == 1 and children[0].move is None:
        return None

    children.sort(key=lambda child: evaluate(child.state))

    best_move = children[0].move
    best_value = float("-inf")
    alpha = float("-inf")
    for child in children:
        value = minimax(child, depth - 1, alpha, float("inf"))
        if value > best_value:
            best_value = value
            best_move = child.move
        alpha = max(alpha, best_value)

    return best_move
