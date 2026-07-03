"""A correct implementation of the spec in prompt.md — write tests for it."""

_open_count = 0


class StoreClosed(Exception):
    """Raised when using a store after close()."""


def connect():
    global _open_count
    if _open_count >= 1:
        raise RuntimeError("an open store already exists — close it first")
    _open_count += 1
    return Store()


class Store:
    def __init__(self):
        self._data = {}
        self._closed = False

    def _check_open(self):
        if self._closed:
            raise StoreClosed("store is closed")

    def put(self, key, value):
        self._check_open()
        self._data[key] = value

    def get(self, key):
        self._check_open()
        return self._data[key]

    def delete(self, key):
        self._check_open()
        if key in self._data:
            del self._data[key]
            return True
        return False

    def close(self):
        global _open_count
        if not self._closed:
            self._closed = True
            _open_count -= 1
