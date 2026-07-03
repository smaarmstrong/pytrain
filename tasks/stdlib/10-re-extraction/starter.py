def parse_log_line(line):
    """Return {'date', 'level', 'message'} for a matching line, else None."""
    raise NotImplementedError


def find_ints(text):
    """All integers (optional leading minus) in text, as ints."""
    raise NotImplementedError


def int_spans(text):
    """(start, end) spans of every integer in text."""
    raise NotImplementedError


def double_ints(text):
    """Replace every integer with twice its value."""
    raise NotImplementedError
