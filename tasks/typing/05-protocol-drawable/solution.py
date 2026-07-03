from collections.abc import Iterable
from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...


class Circle:
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> str:
        return f"circle(r={self.radius})"


class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def draw(self) -> str:
        return f"square(s={self.side})"


def render_all(items: Iterable[Drawable]) -> list[str]:
    return [item.draw() for item in items]
