from __future__ import annotations

import pygame

from engine.scene import Scene


class FadeTransition(Scene):
    """
    Crossfades through black between `from_scene` and `to_scene`
    instead of cutting to the new scene instantly. Input is ignored
    while the transition plays. `to_scene.on_enter()` only fires once
    the fade actually hands control over, via the normal
    `Game.change_scene` flow.
    """

    def __init__(self, game, from_scene: Scene, to_scene: Scene, duration: float = 0.7) -> None:
        super().__init__(game)
        self.from_scene = from_scene
        self.to_scene = to_scene
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> None:
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.game.change_scene(self.to_scene)

    def draw(self, surface: pygame.Surface) -> None:
        half = self.duration / 2
        if self.elapsed < half:
            self.from_scene.draw(surface)
            alpha = round(255 * (self.elapsed / half))
        else:
            self.to_scene.draw(surface)
            alpha = round(255 * (1 - (self.elapsed - half) / half))

        if alpha > 0:
            overlay = pygame.Surface(surface.get_size())
            overlay.fill((0, 0, 0))
            overlay.set_alpha(alpha)
            surface.blit(overlay, (0, 0))
