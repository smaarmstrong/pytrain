from collections.abc import Iterable
from typing import Protocol, runtime_checkable

# TODO: Drawable protocol (runtime_checkable, one method: draw(self) -> str)


class Circle:
    def __init__(self, radius):
        raise NotImplementedError


class Square:
    def __init__(self, side):
        raise NotImplementedError


def render_all(items):
    raise NotImplementedError
