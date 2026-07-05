from __future__ import annotations

import pygame

import config
from engine.events import Signal
from engine.input import is_left_click


class Button:
    """A rectangular clickable label; emits `on_click` when pressed."""

    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font) -> None:
        self.rect = rect
        self.text = text
        self.font = font
        self.on_click = Signal()
        self._hovered = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._hovered = self.rect.collidepoint(event.pos)
        elif is_left_click(event) and self.rect.collidepoint(event.pos):
            self.on_click.emit()

    def draw(self, surface: pygame.Surface) -> None:
        color = config.COLOR_BUTTON_HOVER if self._hovered else config.COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        label = self.font.render(self.text, True, config.COLOR_BUTTON_TEXT)
        surface.blit(label, label.get_rect(center=self.rect.center))
