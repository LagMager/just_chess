from __future__ import annotations

import pygame

import config
from engine.scene import Scene
from ui.shapes import draw_bolt, draw_checker_background, draw_knight, draw_star, scrolling_offset
from ui.text import draw_lines, wrap_text
from ui.widgets.button import Button

RULES = [
    "Cada jugador controla un caballo y se mueve en L, como en el ajedrez.",
    "Mover cuesta 1 de energia. Si llegas a una casilla con puntos (estrella), "
    "la sumas a tu marcador. Si llegas a una casilla de energia (rayo), la recuperas.",
    "Cada casilla de puntos o energia solo se puede usar una vez: al pisarla, desaparece "
    "para ambos jugadores.",
    "Si no te queda energia para moverte, pierdes el turno y se te descuentan 3 puntos.",
    "La maquina siempre mueve primero. La dificultad elegida controla que tan profundo "
    "piensa sus jugadas (Minimax).",
    "La partida termina cuando ya no quedan puntos en el tablero o ninguno de los dos "
    "puede moverse. Gana quien tenga mas puntos.",
]


class HowToPlayScreen(Scene):
    """Explains the rules of the game to a first-time player."""

    def __init__(self, game) -> None:
        super().__init__(game)
        button_rect = pygame.Rect(0, 0, 200, 46)
        button_rect.center = (config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT - 50)
        self._back_button = Button(
            button_rect, "Volver", game.assets.get_font(config.FONT_SIZE_MEDIUM)
        )
        self._back_button.on_click.connect(self._go_back)

    def _go_back(self) -> None:
        from ui.screens.menu_screen import MenuScreen

        self.game.change_scene(MenuScreen(self.game))

    def handle_event(self, event: pygame.event.Event) -> None:
        self._back_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        draw_checker_background(
            surface, 60, config.COLOR_BACKGROUND, config.COLOR_BACKGROUND_ALT, scrolling_offset()
        )
        center_x = config.WINDOW_WIDTH // 2

        title_font = self.game.assets.get_font(config.FONT_SIZE_LARGE, bold=True)
        title = title_font.render("Como jugar", True, config.COLOR_TEXT)
        surface.blit(title, title.get_rect(center=(center_x, 55)))

        self._draw_legend(surface, y=110)
        self._draw_rules(surface, y=170)

        self._back_button.draw(surface)

    def _draw_legend(self, surface: pygame.Surface, y: int) -> None:
        label_font = self.game.assets.get_font(config.FONT_SIZE_SMALL)
        entries = [
            ("Puntos", lambda pos: draw_star(surface, pos, 16, config.COLOR_POINTS)),
            ("Energia", lambda pos: draw_bolt(surface, pos, 16, config.COLOR_ENERGY)),
            ("Tu", lambda pos: draw_knight(surface, pos, 16, config.COLOR_PLAYER, (20, 20, 20))),
            ("Maquina", lambda pos: draw_knight(surface, pos, 16, config.COLOR_AI, (220, 220, 220))),
        ]

        gap = 190
        start_x = config.WINDOW_WIDTH // 2 - gap * (len(entries) - 1) // 2
        for index, (label, draw_icon) in enumerate(entries):
            x = start_x + index * gap
            draw_icon((x, y))
            text = label_font.render(label, True, config.COLOR_TEXT_MUTED)
            surface.blit(text, text.get_rect(midleft=(x + 24, y)))

    def _draw_rules(self, surface: pygame.Surface, y: int) -> None:
        card_rect = pygame.Rect(80, y, config.WINDOW_WIDTH - 160, 470)
        pygame.draw.rect(surface, config.CARD_BG, card_rect, border_radius=12)
        pygame.draw.rect(surface, config.CARD_BORDER, card_rect, width=1, border_radius=12)

        bullet_font = self.game.assets.get_font(config.FONT_SIZE_SMALL)
        text_x = card_rect.x + 30
        text_y = card_rect.y + 24
        max_width = card_rect.width - 60

        for rule in RULES:
            lines = wrap_text(bullet_font, f"- {rule}", max_width)
            draw_lines(surface, bullet_font, lines, (text_x, text_y), config.COLOR_TEXT, line_spacing=4)
            text_y += (bullet_font.get_height() + 4) * len(lines) + 14
