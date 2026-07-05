from __future__ import annotations

import math

import pygame
import pygame.gfxdraw

Point = tuple[float, float]
Color = tuple[int, int, int]


def _scaled_polygon(
    center: tuple[int, int], size: float, unit_points: list[Point]
) -> list[tuple[int, int]]:
    cx, cy = center
    return [(cx + x * size, cy + y * size) for x, y in unit_points]


def draw_polygon(
    surface: pygame.Surface, points: list[tuple[float, float]], color: Color
) -> None:
    """Fills and outlines a polygon with anti-aliased edges."""
    int_points = [(round(x), round(y)) for x, y in points]
    pygame.gfxdraw.filled_polygon(surface, int_points, color)
    pygame.gfxdraw.aapolygon(surface, int_points, color)


def draw_bar(
    surface: pygame.Surface,
    rect: pygame.Rect,
    fraction: float,
    background_color: Color,
    fill_color: Color,
) -> None:
    """Draws a horizontal progress bar clamped to [0, 1] of `rect`."""
    fraction = max(0.0, min(1.0, fraction))
    radius = rect.height // 2
    pygame.draw.rect(surface, background_color, rect, border_radius=radius)
    if fraction > 0:
        fill_rect = rect.copy()
        fill_rect.width = max(rect.height, round(rect.width * fraction))
        pygame.draw.rect(surface, fill_color, fill_rect, border_radius=radius)


def draw_shadow(
    surface: pygame.Surface, center: tuple[int, int], radius: int, color: Color
) -> None:
    """Draws a soft elliptical shadow beneath a piece or tile icon."""
    shadow_rect = pygame.Rect(0, 0, radius * 2, int(radius * 0.9))
    shadow_rect.center = (center[0], center[1] + int(radius * 0.85))
    shadow_surface = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surface, (*color, 90), shadow_surface.get_rect())
    surface.blit(shadow_surface, shadow_rect.topleft)


_STAR_UNIT_POINTS = [
    (math.sin(math.radians(angle)) * (1.0 if index % 2 == 0 else 0.42),
     -math.cos(math.radians(angle)) * (1.0 if index % 2 == 0 else 0.42))
    for index, angle in enumerate(range(0, 360, 36))
]


def draw_star(
    surface: pygame.Surface, center: tuple[int, int], size: int, color: Color
) -> None:
    draw_polygon(surface, _scaled_polygon(center, size, _STAR_UNIT_POINTS), color)


_BOLT_UNIT_POINTS = [
    (0.55, -1.0),
    (-0.5, 0.15),
    (-0.05, 0.15),
    (0.35, 1.0),
    (0.5, -0.05),
    (0.0, -0.05),
]


def draw_bolt(
    surface: pygame.Surface, center: tuple[int, int], size: int, color: Color
) -> None:
    draw_polygon(surface, _scaled_polygon(center, size, _BOLT_UNIT_POINTS), color)


def _draw_aa_circle(
    surface: pygame.Surface, center: tuple[float, float], radius: float, color: Color
) -> None:
    x, y, r = round(center[0]), round(center[1]), round(radius)
    pygame.gfxdraw.filled_circle(surface, x, y, r, color)
    pygame.gfxdraw.aacircle(surface, x, y, r, color)


def draw_knight(
    surface: pygame.Surface,
    center: tuple[int, int],
    size: int,
    fill_color: Color,
    outline_color: Color,
) -> None:
    """Draws a stylized knight (horse head) as a head, snout, and ear."""
    draw_shadow(surface, center, size, (0, 0, 0))
    cx, cy = center

    head_radius = size * 0.6
    head_center = (cx - size * 0.05, cy - size * 0.05)

    snout = [
        (head_center[0] + head_radius * 0.25, head_center[1] + head_radius * 0.05),
        (cx + size * 0.95, cy + size * 0.1),
        (cx + size * 0.7, cy + size * 0.55),
        (head_center[0] + head_radius * 0.05, head_center[1] + head_radius * 0.6),
    ]
    ear = [
        (head_center[0] - head_radius * 0.2, head_center[1] - head_radius * 0.85),
        (head_center[0] + head_radius * 0.4, head_center[1] - head_radius * 0.95),
        (head_center[0] + head_radius * 0.15, head_center[1] - head_radius * 0.1),
    ]

    _draw_aa_circle(surface, head_center, head_radius, fill_color)
    draw_polygon(surface, snout, fill_color)
    draw_polygon(surface, ear, fill_color)

    outer_snout_edge = [snout[1], snout[2]]
    outer_ear_edges = [(ear[0], ear[1]), (ear[1], ear[2])]
    pygame.draw.line(surface, outline_color, outer_snout_edge[0], outer_snout_edge[1], 2)
    for start, end in outer_ear_edges:
        pygame.draw.line(surface, outline_color, start, end, 2)
    pygame.gfxdraw.aacircle(
        surface, round(head_center[0]), round(head_center[1]), round(head_radius), outline_color
    )

    eye_center = (head_center[0] + head_radius * 0.3, head_center[1] - head_radius * 0.05)
    _draw_aa_circle(surface, eye_center, max(2, size * 0.07), outline_color)
