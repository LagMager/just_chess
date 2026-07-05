import pygame


def is_left_click(event: pygame.event.Event) -> bool:
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1


def mouse_position() -> tuple[int, int]:
    return pygame.mouse.get_pos()
