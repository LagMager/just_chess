from __future__ import annotations

import pygame

from engine.asset_loader import AssetLoader
from engine.scene import Scene
from engine.timer import Timer


class Game:
    """
    Owns the pygame window and the main loop; delegates all
    per-frame behavior to whichever Scene is currently active.
    """

    def __init__(
        self, width: int, height: int, title: str, fps: int, icon: pygame.Surface | None = None
    ) -> None:
        pygame.init()
        if icon is not None:
            pygame.display.set_icon(icon)
        pygame.display.set_caption(title)
        self.screen = pygame.display.set_mode((width, height))
        self.assets = AssetLoader()
        self._timer = Timer(fps)
        self._scene: Scene | None = None
        self._running = False

    def change_scene(self, scene: Scene) -> None:
        if self._scene is not None:
            self._scene.on_exit()
        self._scene = scene
        self._scene.on_enter()

    def run(self, initial_scene: Scene) -> None:
        self.change_scene(initial_scene)
        self._running = True
        while self._running:
            dt = self._timer.tick()
            self._process_events()
            if self._scene is not None:
                self._scene.update(dt)
                self._scene.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

    def quit(self) -> None:
        self._running = False

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif self._scene is not None:
                self._scene.handle_event(event)
