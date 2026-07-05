import pygame


class Timer:
    """Wraps pygame's clock to cap the frame rate and report delta time."""

    def __init__(self, fps: int) -> None:
        self._clock = pygame.time.Clock()
        self._fps = fps

    def tick(self) -> float:
        """Advances the clock and returns elapsed seconds since the last tick."""
        return self._clock.tick(self._fps) / 1000.0

    def get_fps(self) -> float:
        return self._clock.get_fps()
