from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str:
        ...


def draw_all(items):
    items = list(items)
    for item in items:
        if not isinstance(item, Drawable):
            raise TypeError(f"{type(item).__name__} object is not Drawable")
    return [item.draw() for item in items]
