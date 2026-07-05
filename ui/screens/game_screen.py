from __future__ import annotations

import math
import threading

import pygame

import config
from ai.minimax import select_best_move
from engine.input import is_left_click
from engine.scene import Scene
from game.board.position import Position
from game.controller import GameController
from game.entities.player import Player
from game.rules import gameplay
from game.rules.movement import get_valid_moves, is_valid_move
from game.state.turn import Turn
from ui.animation import FloatingText, PickupBurst, PieceAnimation
from ui.camera import Camera
from ui.renderer import BoardRenderer
from ui.shapes import draw_screen_vignette
from ui.text import draw_lines, wrap_text
from ui.widgets.button import Button
from ui.widgets.hud import Hud

LOW_ENERGY_THRESHOLD = 2


class GameScreen(Scene):
    """Hosts a single match: board, HUD, and player/AI turn handling."""

    def __init__(self, game, depth: int) -> None:
        super().__init__(game)
        self.depth = depth
        self.camera = Camera(config.BOARD_ORIGIN, config.TILE_SIZE, config.BOARD_SIZE)
        self.renderer = BoardRenderer(self.camera, game.assets)
        self.controller = GameController()
        self.state = self.controller.new_game(depth)

        self._selected = False
        self._animation: PieceAnimation | None = None
        self._effects: list[FloatingText] = []
        self._bursts: list[PickupBurst] = []
        self._effect_font = game.assets.get_font(config.FONT_SIZE_MEDIUM, bold=True)
        self._time = 0.0

        self._ai_thread: threading.Thread | None = None
        self._ai_done = False
        self._ai_result: Position | None = None
        self._ai_generation = 0

        hud_area = pygame.Rect(
            config.BOARD_ORIGIN[0] + self.camera.board_width() + 30,
            config.BOARD_ORIGIN[1],
            230,
            0,
        )
        self.hud = Hud(hud_area, game.assets)

        button_rect = pygame.Rect(hud_area.x, self.hud.bottom() + 30, 200, 44)
        self._new_game_button = Button(
            button_rect, "Nuevo Juego", game.assets.get_font(config.FONT_SIZE_SMALL)
        )
        self._new_game_button.on_click.connect(self._restart)
        self._hint_font = game.assets.get_font(config.FONT_SIZE_SMALL)

    def _restart(self) -> None:
        from engine.transition import FadeTransition

        # A fresh instance (rather than resetting self.state in place) so
        # the restart gets the same fade treatment as every other scene
        # change, instead of cutting straight to the new board.
        new_screen = GameScreen(self.game, self.depth)
        self.game.change_scene(FadeTransition(self.game, self, new_screen))

    def handle_event(self, event: pygame.event.Event) -> None:
        self._new_game_button.handle_event(event)

        if self.state.game_over or self.state.turn != Turn.PLAYER or self._animation:
            return
        if not is_left_click(event):
            return

        clicked = self.camera.position_at(event.pos)
        if clicked is None:
            return

        if clicked == self.state.player.position:
            self._selected = not self._selected
            return

        if self._selected and is_valid_move(self.state.board, self.state.player.position, clicked):
            self._selected = False
            self._commit_move(self.state.player, clicked)

    def update(self, dt: float) -> None:
        self._time += dt
        self._update_effects(dt)

        if self._animation is not None:
            if not self._animation.update(dt):
                return
            if self._animation.pickup:
                kind, value = self._animation.pickup
                color = config.COLOR_POINTS if kind == "points" else config.COLOR_ENERGY
                destination = self._animation.destination
                self._effects.append(FloatingText(destination, f"+{value}", color))
                self._bursts.append(PickupBurst(destination, color))
            self._animation = None
            return

        if self.state.game_over:
            self._go_to_winner_screen()
            return

        if self.state.turn == Turn.PLAYER:
            if self.state.player.energy < gameplay.MOVE_ENERGY_COST:
                self._commit_move(self.state.player, self.state.player.position)
        elif self.state.turn == Turn.AI:
            self._play_ai_turn()

    def _update_effects(self, dt: float) -> None:
        self._effects = [effect for effect in self._effects if not effect.update(dt)]
        self._bursts = [burst for burst in self._bursts if not burst.update(dt)]

    def _play_ai_turn(self) -> None:
        """
        Runs minimax on a background thread so depth-6 searches (which
        can take over a second) don't freeze the render loop. `_commit_move`
        only runs on the main thread once the result comes back.
        """
        if self._ai_thread is not None:
            if self._ai_done:
                move = self._ai_result
                self._ai_thread = None
                self._ai_done = False
                destination = move if move is not None else self.state.ai.position
                self._commit_move(self.state.ai, destination)
            return

        generation = self._ai_generation
        state, depth = self.state, self.state.difficulty

        def worker() -> None:
            move = select_best_move(state, depth)
            if generation == self._ai_generation:
                self._ai_result = move
                self._ai_done = True

        self._ai_thread = threading.Thread(target=worker, daemon=True)
        self._ai_thread.start()

    def _commit_move(self, entity: Player, destination: Position) -> None:
        origin = entity.position
        is_skip = entity.energy < gameplay.MOVE_ENERGY_COST or origin == destination

        pickup = None
        if not is_skip:
            tile = self.state.board.get_tile(destination)
            if not tile.consumed:
                if tile.points:
                    pickup = ("points", tile.points)
                elif tile.energy:
                    pickup = ("energy", tile.energy)

        self.controller.make_move(destination)

        if is_skip:
            self._effects.append(FloatingText(origin, "-3", config.COLOR_LOSE))
        else:
            self._animation = PieceAnimation(entity is self.state.ai, origin, destination, pickup)

    def _go_to_winner_screen(self) -> None:
        from engine.transition import FadeTransition
        from ui.screens.winner_screen import WinnerScreen

        winner_screen = WinnerScreen(self.game, self.state.player, self.state.ai, self.state.winner)
        self.game.change_scene(FadeTransition(self.game, self, winner_screen))

    def _hint_text(self) -> str:
        if self.state.game_over:
            return ""
        if self.state.turn == Turn.AI:
            return "La maquina esta pensando..."
        if self.state.player.energy < gameplay.MOVE_ENERGY_COST:
            return "Sin energia: pierdes el turno (-3 puntos)."
        if not self._selected:
            return "Haz click en tu caballo para ver sus movimientos."
        return "Haz click en una casilla resaltada en verde para moverte."

    def _piece_pixels(self) -> tuple[tuple[float, float], tuple[float, float]]:
        player_pixel = self.camera.tile_center(self.state.player.position)
        ai_pixel = self.camera.tile_center(self.state.ai.position)
        if self._animation is not None:
            pixel = self._animation.current_pixel(self.camera)
            if self._animation.is_ai:
                ai_pixel = pixel
            else:
                player_pixel = pixel
        return player_pixel, ai_pixel

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(config.COLOR_BACKGROUND)
        self.renderer.draw_frame(surface)
        self.renderer.draw_grid(surface)

        selected_position = self.state.player.position if self._selected else None
        valid_moves = []
        if self._selected and not self.state.game_over and self.state.turn == Turn.PLAYER:
            valid_moves = get_valid_moves(self.state.board, self.state.player.position)
        self.renderer.draw_highlights(surface, selected_position, valid_moves)

        keep_visible = self._animation.destination if self._animation and self._animation.pickup else None
        self.renderer.draw_tiles(surface, self.state.board, keep_visible)

        player_pixel, ai_pixel = self._piece_pixels()
        (player_draw, player_radius), (ai_draw, ai_radius) = self.renderer.draw_pieces(
            surface, player_pixel, ai_pixel
        )
        self.renderer.draw_piece_status(surface, player_draw, player_radius, self.state.player)
        self.renderer.draw_piece_status(surface, ai_draw, ai_radius, self.state.ai)
        self.renderer.draw_coordinates(surface)

        for burst in self._bursts:
            burst.draw(surface, self.camera)
        for effect in self._effects:
            effect.draw(surface, self.camera, self._effect_font)

        self.hud.draw(surface, self.state.player, self.state.ai, self.state.turn)
        self._new_game_button.draw(surface)

        hint = self._hint_text()
        if hint:
            lines = wrap_text(self._hint_font, hint, self.hud.area.width)
            position = (self.hud.area.x, self._new_game_button.rect.bottom + 20)
            draw_lines(surface, self._hint_font, lines, position, config.COLOR_HINT)

        if not self.state.game_over and self.state.player.energy <= LOW_ENERGY_THRESHOLD:
            pulse = 0.5 + 0.5 * math.sin(self._time * 5)
            draw_screen_vignette(surface, config.COLOR_LOSE, 0.35 + 0.35 * pulse)
