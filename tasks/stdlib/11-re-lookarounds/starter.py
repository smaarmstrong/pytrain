def bold_texts(html):
    """Contents of every <b>...</b>, in order (lazy match, not greedy)."""
    raise NotImplementedError


def quoted(text):
    """Every double-quoted string, quotes stripped, in order."""
    raise NotImplementedError


def dollar_amounts(text):
    """Ints directly preceded by '$', without the '$' (lookbehind)."""
    raise NotImplementedError


def split_camel(name):
    """Insert a space at each lower-to-UPPER boundary (lookarounds)."""
    raise NotImplementedError
