from __future__ import annotations

import pygame

import config
from engine.asset_loader import AssetLoader
from game.entities.player import Player
from game.state.turn import Turn


class Hud:
    """Renders turn, score, and energy readouts for both players."""

    LINE_HEIGHT = 30

    def __init__(self, area: pygame.Rect, assets: AssetLoader) -> None:
        self.area = area
        self._title_font = assets.get_font(config.FONT_SIZE_MEDIUM, bold=True)
        self._text_font = assets.get_font(config.FONT_SIZE_SMALL)

    def draw(
        self, surface: pygame.Surface, player: Player, ai: Player, turn: Turn
    ) -> None:
        x, y = self.area.x, self.area.y

        turn_label = "Turno: Tu" if turn == Turn.PLAYER else "Turno: Maquina"
        surface.blit(self._title_font.render(turn_label, True, config.COLOR_TEXT), (x, y))
        y += self.LINE_HEIGHT * 2

        for label, entity in (("Tu", player), ("Maquina", ai)):
            surface.blit(self._title_font.render(label, True, config.COLOR_TEXT), (x, y))
            y += self.LINE_HEIGHT
            surface.blit(
                self._text_font.render(
                    f"Puntos: {entity.score}", True, config.COLOR_TEXT_MUTED
                ),
                (x, y),
            )
            y += self.LINE_HEIGHT
            surface.blit(
                self._text_font.render(
                    f"Energia: {entity.energy}", True, config.COLOR_TEXT_MUTED
                ),
                (x, y),
            )
            y += int(self.LINE_HEIGHT * 1.5)
