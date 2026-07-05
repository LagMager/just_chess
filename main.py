import config
from engine.game import Game
from ui.screens.menu_screen import MenuScreen
from ui.shapes import build_app_icon


def main() -> None:
    game = Game(
        config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE, config.FPS,
        icon_factory=build_app_icon,
    )
    game.run(MenuScreen(game))


if __name__ == "__main__":
    main()
