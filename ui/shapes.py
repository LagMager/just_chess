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


def draw_checker_background(
    surface: pygame.Surface, tile_size: int, color_a: Color, color_b: Color
) -> None:
    """Fills `surface` with a low-contrast checkerboard, echoing the game
    board so menu-like screens don't read as bare empty space."""
    width, height = surface.get_size()
    for row in range(height // tile_size + 1):
        for column in range(width // tile_size + 1):
            color = color_a if (row + column) % 2 == 0 else color_b
            rect = pygame.Rect(column * tile_size, row * tile_size, tile_size, tile_size)
            pygame.draw.rect(surface, color, rect)


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


_KNIGHT_GLYPH = chr(0x265E)  # solid chess-knight silhouette, recolored per player
_KNIGHT_FONT_CANDIDATES = ["Segoe UI Symbol", "Apple Symbols", "DejaVu Sans", "Noto Sans Symbols2"]
_knight_font_cache: dict[int, "pygame.font.Font | None"] = {}


def _get_knight_font(point_size: int) -> "pygame.font.Font | None":
    """
    Looks up a system font that actually ships the chess-knight glyph.
    Cached per size since SysFont lookups hit the filesystem. Returns
    None if none of the candidates are installed, so callers can fall
    back to the hand-drawn silhouette.
    """
    if point_size not in _knight_font_cache:
        available = set(pygame.font.get_fonts())
        font = None
        for name in _KNIGHT_FONT_CANDIDATES:
            if name.lower().replace(" ", "") in available:
                font = pygame.font.SysFont(name, point_size)
                break
        _knight_font_cache[point_size] = font
    return _knight_font_cache[point_size]


def draw_knight(
    surface: pygame.Surface,
    center: tuple[int, int],
    size: int,
    fill_color: Color,
    outline_color: Color,
) -> None:
    """Draws a knight piece: the system chess-glyph if available, else a
    hand-drawn silhouette fallback."""
    draw_shadow(surface, center, size, (0, 0, 0))
    font = _get_knight_font(round(size * 2.5))
    if font is not None:
        _draw_knight_glyph(surface, center, font, fill_color, outline_color)
    else:
        _draw_knight_vector(surface, center, size, fill_color, outline_color)


def _draw_knight_glyph(
    surface: pygame.Surface,
    center: tuple[int, int],
    font: pygame.font.Font,
    fill_color: Color,
    outline_color: Color,
) -> None:
    fill_glyph = font.render(_KNIGHT_GLYPH, True, fill_color)
    outline_glyph = font.render(_KNIGHT_GLYPH, True, outline_color)
    rect = fill_glyph.get_rect(center=center)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        surface.blit(outline_glyph, (rect.x + dx, rect.y + dy))
    surface.blit(fill_glyph, rect)


def _draw_knight_vector(
    surface: pygame.Surface,
    center: tuple[int, int],
    size: int,
    fill_color: Color,
    outline_color: Color,
) -> None:
    """Hand-drawn head/snout/ear silhouette, used when no system font
    ships an actual chess-knight glyph."""
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
