from __future__ import annotations

import pygame

from game.board.position import Position


class Camera:
    """
    Maps between board coordinates and screen pixels for a square
    grid anchored at `origin` with cells of `tile_size`.
    """

    def __init__(
        self, origin: tuple[int, int], tile_size: int, board_size: int
    ) -> None:
        self.origin = origin
        self.tile_size = tile_size
        self.board_size = board_size

    def tile_rect(self, position: Position) -> pygame.Rect:
        x = self.origin[0] + position.column * self.tile_size
        y = self.origin[1] + position.row * self.tile_size
        return pygame.Rect(x, y, self.tile_size, self.tile_size)

    def tile_center(self, position: Position) -> tuple[int, int]:
        return self.tile_rect(position).center

    def board_width(self) -> int:
        return self.board_size * self.tile_size

    def position_at(self, pixel: tuple[int, int]) -> Position | None:
        x, y = pixel
        origin_x, origin_y = self.origin
        if x < origin_x or y < origin_y:
            return None

        column = (x - origin_x) // self.tile_size
        row = (y - origin_y) // self.tile_size
        if 0 <= row < self.board_size and 0 <= column < self.board_size:
            return Position(row, column)
        return None
