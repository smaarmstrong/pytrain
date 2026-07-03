def make_counter():
    """Zero-arg function returning 1, 2, 3, ... (needs nonlocal)."""
    raise NotImplementedError


def make_accumulator(start=0):
    """One-arg function adding to a running total, returning it."""
    raise NotImplementedError


def make_multipliers(factors):
    """List of one-arg functions; i-th multiplies by factors[i].
    Beware late binding in loops!"""
    raise NotImplementedError
