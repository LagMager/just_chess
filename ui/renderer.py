from __future__ import annotations

import pygame

import config
from engine.asset_loader import AssetLoader
from game.board.board import Board
from game.board.position import Position
from game.entities.player import Player
from ui.camera import Camera
from ui.shapes import draw_bar, draw_bolt, draw_knight, draw_star

COLUMN_LABELS = "abcdefgh"


class BoardRenderer:
    """Draws the board frame, grid, remaining tiles, and both knights."""

    def __init__(self, camera: Camera, assets: AssetLoader) -> None:
        self.camera = camera
        self.piece_radius = camera.tile_size // 2 - 10
        self._tile_font = assets.get_font(config.FONT_SIZE_SMALL, bold=True)
        self._coord_font = assets.get_font(config.FONT_SIZE_SMALL - 4)
        self._badge_font = assets.get_font(config.FONT_SIZE_SMALL - 4, bold=True)

    def draw_frame(self, surface: pygame.Surface) -> None:
        padding = config.BOARD_FRAME_PADDING
        frame_rect = pygame.Rect(
            self.camera.origin[0] - padding,
            self.camera.origin[1] - padding,
            self.camera.board_width() + padding * 2,
            self.camera.board_width() + padding * 2,
        )
        pygame.draw.rect(surface, config.BOARD_FRAME_COLOR, frame_rect, border_radius=6)

    def draw_coordinates(self, surface: pygame.Surface) -> None:
        origin_x, origin_y = self.camera.origin
        board_width = self.camera.board_width()

        for column in range(self.camera.board_size):
            label = self._coord_font.render(
                COLUMN_LABELS[column], True, config.COLOR_COORD_LABEL
            )
            x = origin_x + column * self.camera.tile_size + self.camera.tile_size // 2
            y = origin_y + board_width + config.BOARD_FRAME_PADDING + 10
            surface.blit(label, label.get_rect(center=(x, y)))

        for row in range(self.camera.board_size):
            label = self._coord_font.render(
                str(self.camera.board_size - row), True, config.COLOR_COORD_LABEL
            )
            x = origin_x - config.BOARD_FRAME_PADDING - 12
            y = origin_y + row * self.camera.tile_size + self.camera.tile_size // 2
            surface.blit(label, label.get_rect(center=(x, y)))

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
            pygame.draw.rect(
                surface,
                config.COLOR_TILE_VALID_MOVE,
                self.camera.tile_rect(position),
                width=4,
                border_radius=6,
            )

    def draw_tiles(
        self, surface: pygame.Surface, board: Board, keep_visible: Position | None = None
    ) -> None:
        """
        Draws every remaining point/energy tile. A tile already marked
        consumed is still drawn if it's `keep_visible`, so a pickup
        icon stays on screen until the knight's move animation
        actually lands on it.
        """
        for row in range(board.SIZE):
            for column in range(board.SIZE):
                tile = board.get_tile(Position(row, column))
                if not tile.points and not tile.energy:
                    continue
                if tile.consumed and tile.position != keep_visible:
                    continue

                center = self.camera.tile_center(tile.position)
                icon_center = (center[0], center[1] - 8)
                icon_size = self.camera.tile_size // 4

                if tile.points:
                    draw_star(surface, icon_center, icon_size, config.COLOR_POINTS)
                    value = tile.points
                else:
                    draw_bolt(surface, icon_center, icon_size, config.COLOR_ENERGY)
                    value = tile.energy

                label = self._tile_font.render(str(value), True, (30, 30, 30))
                label_pos = (center[0], center[1] + icon_size + 6)
                surface.blit(label, label.get_rect(center=label_pos))

    def draw_pieces(
        self,
        surface: pygame.Surface,
        player_pixel: tuple[float, float],
        ai_pixel: tuple[float, float],
    ) -> None:
        radius = self.piece_radius
        draw_knight(surface, player_pixel, radius, config.COLOR_PLAYER, (20, 20, 20))
        draw_knight(surface, ai_pixel, radius, config.COLOR_AI, (220, 220, 220))

    def draw_piece_status(
        self, surface: pygame.Surface, pixel: tuple[float, float], entity: Player
    ) -> None:
        """
        Draws a compact energy bar under the knight and a points badge
        above it, so each player's status is readable at a glance right
        where their piece is -- not just in the side HUD.
        """
        radius = self.piece_radius

        bar_rect = pygame.Rect(0, 0, round(radius * 1.9), 6)
        bar_rect.center = (round(pixel[0]), round(pixel[1] + radius + 11))
        fraction = entity.energy / config.MAX_ENERGY_FOR_BAR
        bar_color = (
            config.ENERGY_BAR_LOW
            if entity.energy <= config.ENERGY_BAR_LOW_THRESHOLD
            else config.ENERGY_BAR_FILL
        )
        draw_bar(surface, bar_rect, fraction, config.ENERGY_BAR_BG, bar_color)

        badge_center = (round(pixel[0] + radius * 0.7), round(pixel[1] - radius * 0.75))
        pygame.draw.circle(surface, config.CARD_BG, badge_center, 13)
        pygame.draw.circle(surface, config.COLOR_POINTS, badge_center, 13, width=2)
        label = self._badge_font.render(str(entity.score), True, config.COLOR_TEXT)
        surface.blit(label, label.get_rect(center=badge_center))
