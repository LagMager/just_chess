from __future__ import annotations

import pygame

import config
from engine.asset_loader import AssetLoader
from game.board.board import Board
from game.board.position import Position
from ui.camera import Camera


class BoardRenderer:
    """Draws the board grid, remaining tiles, and both knights."""

    def __init__(self, camera: Camera, assets: AssetLoader) -> None:
        self.camera = camera
        self._tile_font = assets.get_font(config.FONT_SIZE_SMALL, bold=True)
        self._piece_font = assets.get_font(config.FONT_SIZE_MEDIUM, bold=True)

    def draw_grid(self, surface: pygame.Surface) -> None:
        for row in range(self.camera.board_size):
            for column in range(self.camera.board_size):
                rect = self.camera.tile_rect(Position(row, column))
                color = (
                    config.COLOR_TILE_LIGHT
                    if (row + column) % 2 == 0
                    else config.COLOR_TILE_DARK
                )
                pygame.draw.rect(surface, color, rect)

    def draw_highlights(
        self,
        surface: pygame.Surface,
        selected: Position | None,
        valid_moves: list[Position],
    ) -> None:
        if selected is not None:
            pygame.draw.rect(
                surface,
                config.COLOR_TILE_SELECTED,
                self.camera.tile_rect(selected),
                width=4,
            )
        for position in valid_moves:
            pygame.draw.circle(
                surface,
                config.COLOR_TILE_VALID_MOVE,
                self.camera.tile_center(position),
                self.camera.tile_size // 6,
            )

    def draw_tiles(self, surface: pygame.Surface, board: Board) -> None:
        for row in range(board.SIZE):
            for column in range(board.SIZE):
                tile = board.get_tile(Position(row, column))
                if tile.consumed or (not tile.points and not tile.energy):
                    continue

                center = self.camera.tile_center(tile.position)
                radius = self.camera.tile_size // 3
                if tile.points:
                    color, value = config.COLOR_POINTS, tile.points
                else:
                    color, value = config.COLOR_ENERGY, tile.energy

                pygame.draw.circle(surface, color, center, radius)
                label = self._tile_font.render(str(value), True, (20, 20, 20))
                surface.blit(label, label.get_rect(center=center))

    def draw_pieces(
        self,
        surface: pygame.Surface,
        player_position: Position,
        ai_position: Position,
    ) -> None:
        self._draw_knight(surface, player_position, config.COLOR_PLAYER)
        self._draw_knight(surface, ai_position, config.COLOR_AI)

    def _draw_knight(
        self, surface: pygame.Surface, position: Position, fill: tuple[int, int, int]
    ) -> None:
        center = self.camera.tile_center(position)
        radius = self.camera.tile_size // 2 - 10
        outline = (20, 20, 20) if fill != (20, 20, 20) else (230, 230, 230)
        pygame.draw.circle(surface, fill, center, radius)
        pygame.draw.circle(surface, outline, center, radius, width=2)
        label = self._piece_font.render("N", True, outline)
        surface.blit(label, label.get_rect(center=center))
