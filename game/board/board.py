from game.board.position import Position
from game.board.tile import Tile


class Board:
    """
    Represents the game board.
    Responsible only for storing and providing access to tiles.
    """

    SIZE = 8

    def __init__(self) -> None:
        self._tiles: list[list[Tile]] = [
            [Tile(Position(row, column)) for column in range(self.SIZE)]
            for row in range(self.SIZE)
        ]

    def get_tile(self, position: Position) -> Tile:
        """Returns the tile at the given position."""
        return self._tiles[position.row][position.column]

    def set_tile(self, tile: Tile) -> None:
        """Replaces the tile at its position."""
        self._tiles[tile.position.row][tile.position.column] = tile

    def consume_tile(self, position: Position) -> None:
        """Marks a tile as consumed."""
        self._tiles[position.row][position.column].consumed = True

    def is_inside(self, position: Position) -> bool:
        """Returns whether the position is inside the board."""
        return 0 <= position.row < self.SIZE and 0 <= position.column < self.SIZE
