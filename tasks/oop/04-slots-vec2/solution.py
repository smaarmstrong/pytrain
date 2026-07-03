class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Vec2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vec2({self.x!r}, {self.y!r})"

    def translated(self, dx, dy):
        return Vec2(self.x + dx, self.y + dy)
