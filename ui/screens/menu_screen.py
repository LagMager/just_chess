from __future__ import annotations

import pygame

import config
from engine.scene import Scene
from ui.widgets.button import Button


class MenuScreen(Scene):
    """Lets the player pick a difficulty and start a new game."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self._selected_difficulty = "Amateur"
        self._difficulty_buttons: list[tuple[str, Button]] = []
        self._start_button: Button | None = None
        self._build_widgets()

    def _build_widgets(self) -> None:
        font = self.game.assets.get_font(config.FONT_SIZE_MEDIUM)
        center_x = config.WINDOW_WIDTH // 2
        button_width, button_height, gap = 220, 50, 20
        start_y = 260

        self._difficulty_buttons = []
        for index, name in enumerate(config.DIFFICULTIES):
            rect = pygame.Rect(0, 0, button_width, button_height)
            rect.center = (center_x, start_y + index * (button_height + gap))
            button = Button(rect, name, font)
            button.on_click.connect(lambda name=name: self._select_difficulty(name))
            self._difficulty_buttons.append((name, button))

        start_rect = pygame.Rect(0, 0, button_width, button_height)
        start_rect.center = (
            center_x,
            start_y + len(config.DIFFICULTIES) * (button_height + gap) + gap,
        )
        self._start_button = Button(start_rect, "Iniciar Partida", font)
        self._start_button.on_click.connect(self._start_game)

    def _select_difficulty(self, name: str) -> None:
        self._selected_difficulty = name

    def _start_game(self) -> None:
        from ui.screens.game_screen import GameScreen

        depth = config.DIFFICULTIES[self._selected_difficulty]
        self.game.change_scene(GameScreen(self.game, depth))

    def handle_event(self, event: pygame.event.Event) -> None:
        for _, button in self._difficulty_buttons:
            button.handle_event(event)
        self._start_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.COLOR_BACKGROUND)

        title_font = self.game.assets.get_font(config.FONT_SIZE_LARGE, bold=True)
        title = title_font.render(config.WINDOW_TITLE, True, config.COLOR_TEXT)
        surface.blit(title, title.get_rect(center=(config.WINDOW_WIDTH // 2, 100)))

        subtitle_font = self.game.assets.get_font(config.FONT_SIZE_SMALL)
        subtitle = subtitle_font.render(
            "Selecciona la dificultad", True, config.COLOR_TEXT_MUTED
        )
        surface.blit(
            subtitle, subtitle.get_rect(center=(config.WINDOW_WIDTH // 2, 150))
        )

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

        self._start_button.draw(surface)
