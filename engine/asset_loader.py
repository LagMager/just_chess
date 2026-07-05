import pygame


class AssetLoader:
    """Caches pygame font objects so screens don't reload one every frame."""

    def __init__(self) -> None:
        self._fonts: dict[tuple[str | None, int, bool], pygame.font.Font] = {}

    def get_font(
        self, size: int, bold: bool = False, name: str | None = None
    ) -> pygame.font.Font:
        key = (name, size, bold)
        if key not in self._fonts:
            font = pygame.font.SysFont(name, size, bold=bold)
            self._fonts[key] = font
        return self._fonts[key]
