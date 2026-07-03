"""Line-parsing layer (suggested split)."""


def parse_line(line):
    """Parse one access-log line.

    Return a dict (e.g. with keys path, status, size) for a well-formed
    line, or None for a malformed one.
    """
    raise NotImplementedError
