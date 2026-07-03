def append_item(item, items=None) -> list:
    """Append to `items`, or to a FRESH list when omitted (no shared state!)."""
    raise NotImplementedError


def next_id() -> int:
    """1, 2, 3, ... across calls — the counter is module-global."""
    raise NotImplementedError


def make_prefixer(prefix: str):
    """Return f(s) -> prefix + s, reading `prefix` from the enclosing scope."""
    raise NotImplementedError
