from __future__ import annotations

import math

import pygame

from game.board.position import Position
from ui.camera import Camera

Color = tuple[int, int, int]


def _smoothstep(t: float) -> float:
    return t * t * (3 - 2 * t)


class PieceAnimation:
    """
    Slides a knight from `origin` to `destination` over `duration`
    seconds, with a small vertical hop to read as a leap rather than
    a flat slide. `pickup`, if set, is applied only once the
    animation finishes -- so the tile icon stays visible until the
    knight visually lands on it.
    """

    def __init__(
        self,
        is_ai: bool,
        origin: Position,
        destination: Position,
        pickup: tuple[str, int] | None = None,
        duration: float = 0.35,
    ) -> None:
        self.is_ai = is_ai
        self.origin = origin
        self.destination = destination
        self.pickup = pickup
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Advances the animation; returns True once it has finished."""
        self.elapsed = min(self.duration, self.elapsed + dt)
        return self.elapsed >= self.duration

    def current_pixel(self, camera: Camera) -> tuple[float, float]:
        t = _smoothstep(self.elapsed / self.duration)
        start_x, start_y = camera.tile_center(self.origin)
        end_x, end_y = camera.tile_center(self.destination)
        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t
        hop = math.sin(t * math.pi) * camera.tile_size * 0.35
        return x, y - hop


class FloatingText:
    """
    A short-lived label that pops in, rises, and fades -- used for
    point/energy pickups and the energy-skip penalty.
    """

    def __init__(
        self, position: Position, text: str, color: Color, duration: float = 0.9
    ) -> None:
        self.position = position
        self.text = text
        self.color = color
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Advances the effect; returns True once it has expired."""
        self.elapsed += dt
        return self.elapsed >= self.duration

    def draw(self, surface: pygame.Surface, camera: Camera, font: pygame.font.Font) -> None:
        t = min(1.0, self.elapsed / self.duration)
        center_x, center_y = camera.tile_center(self.position)
        rise = 34 * t
        scale = 1.0 + 0.35 * max(0.0, 1.0 - t * 5)

        label = font.render(self.text, True, self.color)
        if abs(scale - 1.0) > 1e-3:
            size = (max(1, round(label.get_width() * scale)), max(1, round(label.get_height() * scale)))
            label = pygame.transform.smoothscale(label, size)
        label.set_alpha(round(255 * (1 - t)))
        surface.blit(label, label.get_rect(center=(center_x, center_y - 10 - rise)))


class PickupBurst:
    """A brief expanding, fading ring marking a points/energy pickup."""

    def __init__(self, position: Position, color: Color, duration: float = 0.45) -> None:
        self.position = position
        self.color = color
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Advances the effect; returns True once it has expired."""
        self.elapsed += dt
        return self.elapsed >= self.duration

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        t = min(1.0, self.elapsed / self.duration)
        radius = round(camera.tile_size * (0.2 + 0.55 * t))
        alpha = round(255 * (1 - t))
        if alpha <= 0:
            return

        ring = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(ring, (*self.color, alpha), (radius + 2, radius + 2), radius, width=4)
        center = camera.tile_center(self.position)
        surface.blit(ring, (center[0] - radius - 2, center[1] - radius - 2))
