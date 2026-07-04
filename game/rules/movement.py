from game.board.board import Board
from game.board.position import Position

KNIGHT_OFFSETS = (
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
)


def get_valid_moves(board: Board, position: Position) -> list[Position]:
    """
    Returns every valid knight move from the given position.
    """
    return [
        Position(position.row + offset[0], position.column + offset[1])
        for offset in KNIGHT_OFFSETS
        if board.is_inside(
            Position(position.row + offset[0], position.column + offset[1])
        )
    ]


def is_valid_move(board: Board, origin: Position, destination: Position) -> bool:
    """
    Returns whether the destination is a legal knight move.
    """
    return destination in get_valid_moves(board, origin)
