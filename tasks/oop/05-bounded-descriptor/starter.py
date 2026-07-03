class Bounded:
    """A descriptor validating that an attribute stays within [minimum, maximum].

    See prompt.md: TypeError for non-numbers, ValueError out of range,
    per-instance storage, AttributeError before first assignment.
    """

    def __init__(self, minimum, maximum):
        raise NotImplementedError

    def __get__(self, obj, objtype=None):
        raise NotImplementedError

    def __set__(self, obj, value):
        raise NotImplementedError
