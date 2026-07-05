import config
from engine.game import Game
from ui.screens.menu_screen import MenuScreen


def main() -> None:
    game = Game(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE, config.FPS)
    game.run(MenuScreen(game))


if __name__ == "__main__":
    main()
