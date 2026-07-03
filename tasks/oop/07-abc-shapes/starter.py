from abc import ABC, abstractmethod  # noqa: F401


class Shape:
    """Make this an ABC with abstract area()/perimeter() and a concrete
    describe() — see prompt.md."""


class Rectangle(Shape):
    def __init__(self, width, height):
        raise NotImplementedError


class Circle(Shape):
    def __init__(self, radius):
        raise NotImplementedError
