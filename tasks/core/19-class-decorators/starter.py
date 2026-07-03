def add_repr(cls):
    """Give cls a __repr__ of the form ClassName(attr=value, ...) built
    from the instance's attributes in assignment order; return cls."""
    raise NotImplementedError


def singleton(cls):
    """Make the decorated class produce a single shared instance:
    first call constructs it (with the given args), later calls return
    the same object without re-running __init__."""
    raise NotImplementedError
