class Book:
    """A dataclass: title, author, pages (default 0), tags (fresh list each)."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class Point:
    """A frozen, ordered, hashable dataclass with fields x then y."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError
