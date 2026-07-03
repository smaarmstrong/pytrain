class Duration:
    """Whole seconds with +, *, comparisons, and reflected ops.

    Dunders you'll want: __add__, __radd__, __mul__, __rmul__,
    __eq__, __lt__, __le__, __gt__, __ge__ (functools.total_ordering
    can shrink that list).
    """

    def __init__(self, seconds: int):
        raise NotImplementedError
