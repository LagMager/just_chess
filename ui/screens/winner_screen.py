from __future__ import annotations

import pygame

import config
from engine.scene import Scene
from game.entities.player import Player
from ui.widgets.button import Button


class WinnerScreen(Scene):
    """Shows the match result and lets the player start a new one."""

    def __init__(self, game, player: Player, ai: Player, winner: Player | None) -> None:
        super().__init__(game)
        self._player = player
        self._ai = ai
        self._winner = winner

        button_rect = pygame.Rect(0, 0, 220, 50)
        button_rect.center = (config.WINDOW_WIDTH // 2, 420)
        self._replay_button = Button(
            button_rect,
            "Jugar de nuevo",
            game.assets.get_font(config.FONT_SIZE_MEDIUM),
        )
        self._replay_button.on_click.connect(self._replay)

    def _replay(self) -> None:
        from ui.screens.menu_screen import MenuScreen

        self.game.change_scene(MenuScreen(self.game))

    def handle_event(self, event: pygame.event.Event) -> None:
        self._replay_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.COLOR_BACKGROUND)

        if self._winner is None:
            text, color = "Empate!", config.COLOR_DRAW
        elif self._winner is self._player:
            text, color = "Ganaste!", config.COLOR_WIN
        else:
            text, color = "Gano la maquina", config.COLOR_LOSE

        title_font = self.game.assets.get_font(config.FONT_SIZE_LARGE, bold=True)
        title = title_font.render(text, True, color)
        surface.blit(title, title.get_rect(center=(config.WINDOW_WIDTH // 2, 200)))

        info_font = self.game.assets.get_font(config.FONT_SIZE_MEDIUM)
        score_line = f"Tu: {self._player.score}   Maquina: {self._ai.score}"
        info = info_font.render(score_line, True, config.COLOR_TEXT)
        surface.blit(info, info.get_rect(center=(config.WINDOW_WIDTH // 2, 280)))

        self._replay_button.draw(surface)
