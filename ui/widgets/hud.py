from __future__ import annotations

import pygame

import config
from engine.asset_loader import AssetLoader
from game.entities.player import Player
from game.state.turn import Turn
from ui.shapes import draw_bar

BANNER_HEIGHT = 50
CARD_HEIGHT = 150
CARD_GAP = 15


class Hud:
    """Renders the turn banner and a stats card for each player."""

    def __init__(self, area: pygame.Rect, assets: AssetLoader) -> None:
        self.area = area
        self._banner_font = assets.get_font(config.FONT_SIZE_MEDIUM, bold=True)
        self._name_font = assets.get_font(config.FONT_SIZE_MEDIUM, bold=True)
        self._label_font = assets.get_font(config.FONT_SIZE_SMALL)

    def draw(
        self, surface: pygame.Surface, player: Player, ai: Player, turn: Turn
    ) -> None:
        self._draw_banner(surface, turn)

        player_card = pygame.Rect(
            self.area.x, self.area.y + BANNER_HEIGHT + CARD_GAP, self.area.width, CARD_HEIGHT
        )
        ai_card = pygame.Rect(
            self.area.x,
            player_card.bottom + CARD_GAP,
            self.area.width,
            CARD_HEIGHT,
        )
        self._draw_card(surface, player_card, "Tu", player, turn == Turn.PLAYER)
        self._draw_card(surface, ai_card, "Maquina", ai, turn == Turn.AI)

    def bottom(self) -> int:
        return self.area.y + BANNER_HEIGHT + CARD_GAP + CARD_HEIGHT * 2 + CARD_GAP

    def _draw_banner(self, surface: pygame.Surface, turn: Turn) -> None:
        rect = pygame.Rect(self.area.x, self.area.y, self.area.width, BANNER_HEIGHT)
        pygame.draw.rect(surface, config.CARD_BG, rect, border_radius=10)
        pygame.draw.rect(surface, config.CARD_ACTIVE_BORDER, rect, width=2, border_radius=10)
        label = "Turno: Tu" if turn == Turn.PLAYER else "Turno: Maquina"
        text = self._banner_font.render(label, True, config.COLOR_TEXT)
        surface.blit(text, text.get_rect(center=rect.center))

    def _draw_card(
        self, surface: pygame.Surface, rect: pygame.Rect, name: str, entity: Player, active: bool
    ) -> None:
        border_color = config.CARD_ACTIVE_BORDER if active else config.CARD_BORDER
        border_width = 3 if active else 1
        pygame.draw.rect(surface, config.CARD_BG, rect, border_radius=10)
        pygame.draw.rect(surface, border_color, rect, width=border_width, border_radius=10)

        padding = 16
        x = rect.x + padding
        y = rect.y + padding

        name_label = self._name_font.render(name, True, config.COLOR_TEXT)
        surface.blit(name_label, (x, y))
        y += name_label.get_height() + 10

        score_label = self._label_font.render(
            f"Puntos: {entity.score}", True, config.COLOR_TEXT_MUTED
        )
        surface.blit(score_label, (x, y))
        y += score_label.get_height() + 10

        energy_label = self._label_font.render(
            f"Energia: {entity.energy}", True, config.COLOR_TEXT_MUTED
        )
        surface.blit(energy_label, (x, y))
        y += energy_label.get_height() + 6

        bar_rect = pygame.Rect(x, y, rect.width - padding * 2, 16)
        fraction = entity.energy / config.MAX_ENERGY_FOR_BAR
        fill_color = (
            config.ENERGY_BAR_LOW
            if entity.energy <= config.ENERGY_BAR_LOW_THRESHOLD
            else config.ENERGY_BAR_FILL
        )
        draw_bar(surface, bar_rect, fraction, config.ENERGY_BAR_BG, fill_color)
