def head_tail(seq):
    if len(seq) < 2:
        raise ValueError("need at least two items")
    first, *middle, last = seq
    return first, middle, last


def merge(*dicts, **overrides):
    out = {}
    for d in dicts:
        out.update(d)
    out.update(overrides)
    return out


def clamp(value, /, lo, hi, *, strict=False):
    if strict and not (lo <= value <= hi):
        raise ValueError(f"{value} outside [{lo}, {hi}]")
    return max(lo, min(hi, value))
