from __future__ import annotations

import pygame

import config
from engine.scene import Scene
from game.entities.player import Player
from ui.shapes import draw_checker_background, draw_knight
from ui.widgets.button import Button


class WinnerScreen(Scene):
    """Shows the match result and lets the player start a new one."""

    def __init__(self, game, player: Player, ai: Player, winner: Player | None) -> None:
        super().__init__(game)
        self._player = player
        self._ai = ai
        self._winner = winner

        button_rect = pygame.Rect(0, 0, 220, 50)
        button_rect.center = (config.WINDOW_WIDTH // 2, 520)
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
        draw_checker_background(surface, 60, config.COLOR_BACKGROUND, config.COLOR_BACKGROUND_ALT)
        center_x = config.WINDOW_WIDTH // 2

        if self._winner is None:
            text, color = "Empate!", config.COLOR_DRAW
        elif self._winner is self._player:
            text, color = "Ganaste!", config.COLOR_WIN
        else:
            text, color = "Gano la maquina", config.COLOR_LOSE

        title_font = self.game.assets.get_font(config.FONT_SIZE_LARGE, bold=True)
        title = title_font.render(text, True, color)
        surface.blit(title, title.get_rect(center=(center_x, 130)))

        self._draw_scoreboard(surface, color, y=260)
        self._replay_button.draw(surface)

    def _draw_scoreboard(self, surface: pygame.Surface, accent: tuple[int, int, int], y: int) -> None:
        card_rect = pygame.Rect(0, 0, 560, 200)
        card_rect.center = (config.WINDOW_WIDTH // 2, y + 100)
        pygame.draw.rect(surface, config.CARD_BG, card_rect, border_radius=14)
        pygame.draw.rect(surface, accent, card_rect, width=2, border_radius=14)

        name_font = self.game.assets.get_font(config.FONT_SIZE_MEDIUM, bold=True)
        score_font = self.game.assets.get_font(config.FONT_SIZE_LARGE, bold=True)

        left_x = card_rect.centerx - 140
        right_x = card_rect.centerx + 140
        icon_y = card_rect.y + 55

        draw_knight(surface, (left_x, icon_y), 34, config.COLOR_PLAYER, (20, 20, 20))
        draw_knight(surface, (right_x, icon_y), 34, config.COLOR_AI, (220, 220, 220))

        name_y = icon_y + 55
        name_label = name_font.render("Tu", True, config.COLOR_TEXT)
        surface.blit(name_label, name_label.get_rect(center=(left_x, name_y)))
        ai_label = name_font.render("Maquina", True, config.COLOR_TEXT)
        surface.blit(ai_label, ai_label.get_rect(center=(right_x, name_y)))

        score_y = name_y + 40
        player_score = score_font.render(str(self._player.score), True, accent)
        surface.blit(player_score, player_score.get_rect(center=(left_x, score_y)))
        ai_score = score_font.render(str(self._ai.score), True, accent)
        surface.blit(ai_score, ai_score.get_rect(center=(right_x, score_y)))

        divider_x = card_rect.centerx
        pygame.draw.line(
            surface, config.CARD_BORDER,
            (divider_x, card_rect.y + 20), (divider_x, card_rect.bottom - 20), 1,
        )
