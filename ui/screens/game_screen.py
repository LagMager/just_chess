from __future__ import annotations

import pygame

import config
from engine.scene import Scene
from game.board.generator import BoardGenerator
from game.entities.player import Player
from game.state.game_state import GameState
from game.state.turn import Turn
from ui.camera import Camera
from ui.renderer import BoardRenderer
from ui.widgets.button import Button
from ui.widgets.hud import Hud


class GameScreen(Scene):
    """Hosts a single match: board, HUD, and the new-game control."""

    def __init__(self, game, depth: int) -> None:
        super().__init__(game)
        self.depth = depth
        self.camera = Camera(config.BOARD_ORIGIN, config.TILE_SIZE, config.BOARD_SIZE)
        self.renderer = BoardRenderer(self.camera, game.assets)
        self.state = self._new_state()

        hud_area = pygame.Rect(
            config.BOARD_ORIGIN[0] + self.camera.board_width() + 30,
            config.BOARD_ORIGIN[1],
            220,
            300,
        )
        self.hud = Hud(hud_area, game.assets)

        button_rect = pygame.Rect(hud_area.x, hud_area.bottom + 40, 200, 44)
        self._new_game_button = Button(
            button_rect, "Nuevo Juego", game.assets.get_font(config.FONT_SIZE_SMALL)
        )
        self._new_game_button.on_click.connect(self._restart)

    def _new_state(self) -> GameState:
        board, spawns = BoardGenerator.generate()
        player_spawn, ai_spawn = spawns
        return GameState(
            board=board,
            player=Player(
                name="Player", position=player_spawn, energy=config.STARTING_ENERGY
            ),
            ai=Player(name="AI", position=ai_spawn, energy=config.STARTING_ENERGY),
            turn=Turn.AI,
            difficulty=self.depth,
        )

    def _restart(self) -> None:
        self.state = self._new_state()

    def handle_event(self, event: pygame.event.Event) -> None:
        self._new_game_button.handle_event(event)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.COLOR_BACKGROUND)
        self.renderer.draw_grid(surface)
        self.renderer.draw_tiles(surface, self.state.board)
        self.renderer.draw_pieces(
            surface, self.state.player.position, self.state.ai.position
        )
        self.hud.draw(surface, self.state.player, self.state.ai, self.state.turn)
        self._new_game_button.draw(surface)
