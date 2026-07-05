from __future__ import annotations

import pygame

import config
from engine.scene import Scene
from ui.shapes import draw_checker_background, draw_knight
from ui.widgets.button import Button

DIFFICULTY_HINTS = {
    "Principiante": "Busqueda a profundidad 2",
    "Amateur": "Busqueda a profundidad 4",
    "Experto": "Busqueda a profundidad 6",
}


class MenuScreen(Scene):
    """Lets the player pick a difficulty and start a new game."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self._selected_difficulty = "Amateur"
        self._difficulty_buttons: list[tuple[str, Button]] = []
        self._start_button: Button | None = None
        self._how_to_play_button: Button | None = None
        self._bg_time = 0.0
        self._build_widgets()

    def _build_widgets(self) -> None:
        font = self.game.assets.get_font(config.FONT_SIZE_MEDIUM)
        center_x = config.WINDOW_WIDTH // 2
        button_width, button_height = 260, 50

        y = 240
        self._difficulty_buttons = []
        for name in config.DIFFICULTIES:
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.center = (center_x, y)
            button = Button(rect, name, font)
            button.on_click.connect(lambda name=name: self._select_difficulty(name))
            self._difficulty_buttons.append((name, button))
            y += button_height + 34

        y += 10
        start_rect = pygame.Rect(0, 0, button_width, button_height)
        start_rect.center = (center_x, y)
        self._start_button = Button(start_rect, "Iniciar Partida", font, primary=True)
        self._start_button.on_click.connect(self._start_game)

        y += button_height + 20
        how_to_play_rect = pygame.Rect(0, 0, button_width, button_height)
        how_to_play_rect.center = (center_x, y)
        self._how_to_play_button = Button(how_to_play_rect, "Como jugar?", font)
        self._how_to_play_button.on_click.connect(self._show_how_to_play)

    def _select_difficulty(self, name: str) -> None:
        self._selected_difficulty = name

    def _start_game(self) -> None:
        from ui.screens.game_screen import GameScreen

        depth = config.DIFFICULTIES[self._selected_difficulty]
        self.game.change_scene(GameScreen(self.game, depth))

    def _show_how_to_play(self) -> None:
        from ui.screens.how_to_play_screen import HowToPlayScreen

        self.game.change_scene(HowToPlayScreen(self.game))

    def handle_event(self, event: pygame.event.Event) -> None:
        for _, button in self._difficulty_buttons:
            button.handle_event(event)
        self._start_button.handle_event(event)
        self._how_to_play_button.handle_event(event)

    def update(self, dt: float) -> None:
        self._bg_time += dt

    def _panel_rect(self) -> pygame.Rect:
        top = self._difficulty_buttons[0][1].rect.top - 60
        bottom = self._how_to_play_button.rect.bottom + 30
        rect = pygame.Rect(0, top, 520, bottom - top)
        rect.centerx = config.WINDOW_WIDTH // 2
        return rect

    def draw(self, surface: pygame.Surface) -> None:
        offset = (self._bg_time * 36, self._bg_time * 24)
        draw_checker_background(
            surface, 60, config.COLOR_BACKGROUND, config.COLOR_BACKGROUND_ALT, offset
        )
        center_x = config.WINDOW_WIDTH // 2

        title_font = self.game.assets.get_font(config.FONT_SIZE_LARGE, bold=True)
        title = title_font.render(config.WINDOW_TITLE, True, config.COLOR_TEXT)
        surface.blit(title, title.get_rect(center=(center_x, 90)))
        draw_knight(surface, (center_x - title.get_width() // 2 - 45, 90), 32, config.COLOR_PLAYER, (20, 20, 20))
        draw_knight(surface, (center_x + title.get_width() // 2 + 45, 90), 32, config.COLOR_AI, (220, 220, 220))

        subtitle_font = self.game.assets.get_font(config.FONT_SIZE_SMALL)
        subtitle = subtitle_font.render(
            "Domina el tablero, junta puntos y no te quedes sin energia.",
            True,
            config.COLOR_TEXT_MUTED,
        )
        surface.blit(subtitle, subtitle.get_rect(center=(center_x, 140)))

        panel_rect = self._panel_rect()
        pygame.draw.rect(surface, config.CARD_BG, panel_rect, border_radius=16)
        pygame.draw.rect(surface, config.CARD_BORDER, panel_rect, width=1, border_radius=16)

        heading_font = self.game.assets.get_font(config.FONT_SIZE_MEDIUM, bold=True)
        heading = heading_font.render("Selecciona la dificultad", True, config.COLOR_TEXT)
        surface.blit(heading, heading.get_rect(center=(center_x, panel_rect.top + 35)))

        hint_font = self.game.assets.get_font(config.FONT_SIZE_SMALL - 2)
        for name, button in self._difficulty_buttons:
            if name == self._selected_difficulty:
                pygame.draw.rect(
                    surface,
                    config.COLOR_TILE_SELECTED,
                    button.rect.inflate(8, 8),
                    width=3,
                    border_radius=10,
                )
            button.draw(surface)
            hint = hint_font.render(DIFFICULTY_HINTS[name], True, config.COLOR_TEXT_MUTED)
            surface.blit(hint, hint.get_rect(center=(center_x, button.rect.bottom + 14)))

        self._start_button.draw(surface)
        self._how_to_play_button.draw(surface)
