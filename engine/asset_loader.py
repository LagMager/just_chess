import pygame

_PREFERRED_UI_FONTS = ["Segoe UI", "Calibri", "Verdana", "Trebuchet MS", "Arial"]


class AssetLoader:
    """Caches pygame font objects so screens don't reload one every frame."""

    def __init__(self) -> None:
        self._fonts: dict[tuple[str | None, int, bool], pygame.font.Font] = {}
        self._default_font_name = self._pick_default_font()

    @staticmethod
    def _pick_default_font() -> str | None:
        """Picks the first installed font from a curated, readable list,
        instead of pygame's plain built-in fallback."""
        available = set(pygame.font.get_fonts())
        for name in _PREFERRED_UI_FONTS:
            if name.lower().replace(" ", "") in available:
                return name
        return None

    def get_font(
        self, size: int, bold: bool = False, name: str | None = None
    ) -> pygame.font.Font:
        font_name = name or self._default_font_name
        key = (font_name, size, bold)
        if key not in self._fonts:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            self._fonts[key] = font
        return self._fonts[key]
