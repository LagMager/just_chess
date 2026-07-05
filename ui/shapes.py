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
    surface: pygame.Surface,
    tile_size: int,
    color_a: Color,
    color_b: Color,
    offset: tuple[float, float] = (0.0, 0.0),
) -> None:
    """
    Fills `surface` with a low-contrast checkerboard, echoing the game
    board so menu-like screens don't read as bare empty space.
    `offset` (in pixels) rigidly translates the whole pattern -- pass
    an increasing value to make the backdrop drift over time. The
    period is 2 tiles, so offsets are wrapped to that to keep the
    values bounded during long play sessions without changing
    anything visually.
    """
    width, height = surface.get_size()
    period = tile_size * 2
    offset_x = offset[0] % period
    offset_y = offset[1] % period

    for row in range(-2, height // tile_size + 3):
        for column in range(-2, width // tile_size + 3):
            color = color_a if (row + column) % 2 == 0 else color_b
            x = column * tile_size - offset_x
            y = row * tile_size - offset_y
            pygame.draw.rect(surface, color, pygame.Rect(x, y, tile_size, tile_size))


def scrolling_offset(speed_x: float = 36.0, speed_y: float = 24.0) -> tuple[float, float]:
    """
    An (x, y) offset driven by pygame's global clock rather than a
    per-screen elapsed-time counter, so a drifting backdrop keeps
    moving continuously across scene changes -- instead of freezing
    (no local timer) or jumping back to zero (a fresh timer) every
    time a new screen instance is constructed.
    """
    t = pygame.time.get_ticks() / 1000.0
    return (t * speed_x, t * speed_y)


def draw_screen_vignette(surface: pygame.Surface, color: Color, intensity: float) -> None:
    """
    Draws a soft pulsing border glow around the edges of `surface`,
    used to signal danger (e.g. critically low energy) without
    covering the center of the screen. `intensity` is clamped to
    [0, 1].
    """
    intensity = max(0.0, min(1.0, intensity))
    if intensity <= 0:
        return

    width, height = surface.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    layers = 8
    max_thickness = 100
    for i in range(layers):
        t = i / layers
        alpha = round(70 * intensity * (1 - t))
        if alpha <= 0:
            continue
        inset = round(t * max_thickness)
        rect = pygame.Rect(inset, inset, width - inset * 2, height - inset * 2)
        thickness = max(2, max_thickness // layers + 2)
        pygame.draw.rect(overlay, (*color, alpha), rect, width=thickness)
    surface.blit(overlay, (0, 0))


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


def build_app_icon(size: int = 64) -> pygame.Surface:
    """Builds the window/taskbar icon: a knight on a rounded dark tile."""
    icon = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.rect(icon, (32, 35, 45), icon.get_rect(), border_radius=size // 5)
    draw_knight(
        icon, (size // 2, size // 2 + round(size * 0.03)), round(size * 0.34),
        (230, 180, 40), (20, 20, 20),
    )
    return icon
