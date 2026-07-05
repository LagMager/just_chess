from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from engine.game import Game


class Scene:
    """
    Base class for a full-screen application state (menu, match,
    winner screen). `Game` drives whichever scene is active by
    calling these lifecycle methods every frame.
    """

    def __init__(self, game: "Game") -> None:
        self.game = game

    def on_enter(self) -> None:
        """Called right after this scene becomes active."""

    def on_exit(self) -> None:
        """Called right before this scene is replaced."""

    def handle_event(self, event: pygame.event.Event) -> None:
        pass  # optional hook; scenes override only what they need

    def update(self, dt: float) -> None:
        pass  # optional hook; scenes override only what they need

    def draw(self, surface: pygame.Surface) -> None:
        pass  # optional hook; scenes override only what they need
