import random

from game.board.board import Board
from game.board.position import Position
from game.board.tile import Tile


class BoardGenerator:
    """
    Generates randomized game boards.
    Responsible for placing:
    - Point tiles
    - Energy tiles
    Also reserves a set of safe empty positions for external use
    (e.g. player spawn points), without knowing anything about players.
    Leaves all other tiles as default (empty).
    """

    NUM_POINTS = 7
    NUM_ENERGY = 4
    NUM_RESERVED = 2  # extra safe positions to hand back, e.g. for spawns

    POINT_VALUES = [2, 3, 4, 5, 6, 8, 9]
    ENERGY_VALUES = [2, 3, 4, 5]

    @staticmethod
    def generate() -> tuple[Board, list[Position]]:
        """
        Creates a new randomized board.
        Returns the board along with a list of safe positions
        (empty tiles) reserved for external use, e.g. player spawns.
        """
        board = Board()
        positions = BoardGenerator._generate_random_positions(board.SIZE)

        BoardGenerator._place_point_tiles(board, positions["points"])
        BoardGenerator._place_energy_tiles(board, positions["energy"])

        return board, positions["reserved"]

    @staticmethod
    def _generate_random_positions(board_size):
        """
        Returns randomized board positions.
        Internal helper.
        """
        total_needed = (
            BoardGenerator.NUM_POINTS
            + BoardGenerator.NUM_ENERGY
            + BoardGenerator.NUM_RESERVED
        )
        all_positions = [
            Position(row, column)
            for row in range(board_size)
            for column in range(board_size)
        ]
        if total_needed > len(all_positions):
            raise ValueError("Board is too small for the number of required positions")

        chosen = random.sample(all_positions, total_needed)
        points = chosen[: BoardGenerator.NUM_POINTS]
        energy = chosen[
            BoardGenerator.NUM_POINTS : BoardGenerator.NUM_POINTS
            + BoardGenerator.NUM_ENERGY
        ]
        reserved = chosen[BoardGenerator.NUM_POINTS + BoardGenerator.NUM_ENERGY :]

        return {"points": points, "energy": energy, "reserved": reserved}

    @staticmethod
    def _place_point_tiles(board: Board, positions: list[Position]) -> None:
        """
        Places all point tiles on the board, each with a unique
        value from POINT_VALUES.
        """
        values = random.sample(
            BoardGenerator.POINT_VALUES, len(BoardGenerator.POINT_VALUES)
        )
        for position, value in zip(positions, values):
            board.set_tile(Tile(position=position, points=value))

    @staticmethod
    def _place_energy_tiles(board: Board, positions: list[Position]) -> None:
        """
        Places all energy tiles on the board, each with a unique
        value from ENERGY_VALUES.
        """
        values = random.sample(
            BoardGenerator.ENERGY_VALUES, len(BoardGenerator.ENERGY_VALUES)
        )
        for position, value in zip(positions, values):
            board.set_tile(Tile(position=position, energy=value))
