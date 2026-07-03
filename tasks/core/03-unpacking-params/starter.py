def head_tail(seq):
    """(first, middle_list, last); ValueError if fewer than 2 items."""
    raise NotImplementedError


def merge(*dicts, **overrides):
    """Merge dicts left-to-right, keyword overrides win. Returns a new dict."""
    raise NotImplementedError


def clamp(value, lo, hi, strict=False):  # fix the parameter kinds!
    """value positional-only, strict keyword-only. See prompt.md."""
    raise NotImplementedError
