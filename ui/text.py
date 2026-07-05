from __future__ import annotations

import pygame


def wrap_text(font: pygame.font.Font, text: str, max_width: int) -> list[str]:
    """Splits `text` into lines that each fit within `max_width` pixels."""
    words = text.split(" ")
    lines: list[str] = []
    current = ""

    for word in words:
        candidate = f"{current} {word}".strip()
        if font.size(candidate)[0] <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)
    return lines


def draw_lines(
    surface: pygame.Surface,
    font: pygame.font.Font,
    lines: list[str],
    position: tuple[int, int],
    color: tuple[int, int, int],
    line_spacing: int = 4,
) -> None:
    x, y = position
    for line in lines:
        label = font.render(line, True, color)
        surface.blit(label, (x, y))
        y += label.get_height() + line_spacing
