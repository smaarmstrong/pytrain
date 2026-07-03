class _CountdownIterator:
    def __init__(self, current: int):
        self._current = current

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < 1:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value


class Countdown:
    def __init__(self, start: int):
        self.start = start

    def __iter__(self):
        return _CountdownIterator(self.start)
