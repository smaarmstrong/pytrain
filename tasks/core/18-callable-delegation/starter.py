class RunningMean:
    """Callable accumulator: each call feeds one number, returns the
    mean of everything fed so far (a float). `.count` = calls so far."""

    def __init__(self):
        raise NotImplementedError


class LoggingProxy:
    """Delegate unknown attribute reads to `target` via __getattr__,
    recording each successfully delegated name in `.accessed`."""

    def __init__(self, target):
        raise NotImplementedError
