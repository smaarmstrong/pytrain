from functools import total_ordering


@total_ordering
class Duration:
    def __init__(self, seconds: int):
        self.seconds = seconds

    def _coerce(self, other):
        if isinstance(other, Duration):
            return other.seconds
        if isinstance(other, int) and not isinstance(other, bool):
            return other
        return None

    def __add__(self, other):
        secs = self._coerce(other)
        if secs is None:
            return NotImplemented
        return Duration(self.seconds + secs)

    __radd__ = __add__

    def __mul__(self, factor):
        if not isinstance(factor, int) or isinstance(factor, bool):
            return NotImplemented
        return Duration(self.seconds * factor)

    __rmul__ = __mul__

    def __eq__(self, other):
        if not isinstance(other, Duration):
            return NotImplemented
        return self.seconds == other.seconds

    def __lt__(self, other):
        if not isinstance(other, Duration):
            return NotImplemented
        return self.seconds < other.seconds

    def __hash__(self):
        return hash(self.seconds)
