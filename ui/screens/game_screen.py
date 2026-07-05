from __future__ import annotations

import pygame

import config
from ai.minimax import select_best_move
from engine.input import is_left_click
from engine.scene import Scene
from game.controller import GameController
from game.rules import gameplay
from game.rules.movement import get_valid_moves, is_valid_move
from game.state.turn import Turn
from ui.camera import Camera
from ui.renderer import BoardRenderer
from ui.widgets.button import Button
from ui.widgets.hud import Hud


class GameScreen(Scene):
    """Hosts a single match: board, HUD, and player/AI turn handling."""

    def __init__(self, game, depth: int) -> None:
        super().__init__(game)
        self.depth = depth
        self.camera = Camera(config.BOARD_ORIGIN, config.TILE_SIZE, config.BOARD_SIZE)
        self.renderer = BoardRenderer(self.camera, game.assets)
        self.controller = GameController()
        self.state = self.controller.new_game(depth)

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

    def _restart(self) -> None:
        self.state = self.controller.new_game(self.depth)

    def handle_event(self, event: pygame.event.Event) -> None:
        self._new_game_button.handle_event(event)

        if self.state.game_over or self.state.turn != Turn.PLAYER:
            return
        if not is_left_click(event):
            return

        destination = self.camera.position_at(event.pos)
        if destination is None:
            return
        if is_valid_move(self.state.board, self.state.player.position, destination):
            self.controller.make_move(destination)

    def update(self, dt: float) -> None:
        if self.state.game_over:
            self._go_to_winner_screen()
            return

        if self.state.turn == Turn.PLAYER:
            if self.state.player.energy < gameplay.MOVE_ENERGY_COST:
                self.controller.make_move(self.state.player.position)
        elif self.state.turn == Turn.AI:
            self._play_ai_turn()

    def _play_ai_turn(self) -> None:
        move = select_best_move(self.state, self.state.difficulty)
        destination = move if move is not None else self.state.ai.position
        self.controller.make_move(destination)

    def _go_to_winner_screen(self) -> None:
        from ui.screens.winner_screen import WinnerScreen

        self.game.change_scene(
            WinnerScreen(self.game, self.state.player, self.state.ai, self.state.winner)
        )

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.COLOR_BACKGROUND)
        self.renderer.draw_grid(surface)

        valid_moves = []
        if not self.state.game_over and self.state.turn == Turn.PLAYER:
            valid_moves = get_valid_moves(self.state.board, self.state.player.position)
        self.renderer.draw_highlights(surface, None, valid_moves)

        self.renderer.draw_tiles(surface, self.state.board)
        self.renderer.draw_pieces(
            surface, self.state.player.position, self.state.ai.position
        )
        self.hud.draw(surface, self.state.player, self.state.ai, self.state.turn)
        self._new_game_button.draw(surface)
