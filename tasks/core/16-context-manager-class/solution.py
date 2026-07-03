class Rollback:
    def __init__(self, data: dict, swallow: bool = False):
        self.data = data
        self.swallow = swallow
        self._snapshot = None

    def __enter__(self):
        self._snapshot = dict(self.data)
        return self.data

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.data.clear()
            self.data.update(self._snapshot)
            return self.swallow
        return False
