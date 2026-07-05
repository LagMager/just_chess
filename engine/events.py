from typing import Callable


class Signal:
    """
    A minimal observer channel: widgets emit an event and screens
    subscribe to it, without either side needing a direct reference
    to pygame's event queue.
    """

    def __init__(self) -> None:
        self._listeners: list[Callable] = []

    def connect(self, listener: Callable) -> None:
        self._listeners.append(listener)

    def emit(self, *args, **kwargs) -> None:
        for listener in self._listeners:
            listener(*args, **kwargs)
