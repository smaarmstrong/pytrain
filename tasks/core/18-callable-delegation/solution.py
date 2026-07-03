class RunningMean:
    def __init__(self):
        self.count = 0
        self._total = 0.0

    def __call__(self, value):
        self.count += 1
        self._total += value
        return self._total / self.count


class LoggingProxy:
    def __init__(self, target):
        self._target = target
        self.accessed = []

    def __getattr__(self, name):
        value = getattr(self._target, name)  # AttributeError propagates
        self.accessed.append(name)
        return value
