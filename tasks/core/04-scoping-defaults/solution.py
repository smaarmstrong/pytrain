_counter = 0


def append_item(item, items=None) -> list:
    if items is None:
        items = []
    items.append(item)
    return items


def next_id() -> int:
    global _counter
    _counter += 1
    return _counter


def make_prefixer(prefix: str):
    def prefixer(s):
        return prefix + s
    return prefixer
