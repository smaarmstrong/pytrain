def to_json(obj):
    """JSON string for obj; supports set and datetime.date via markers."""
    raise NotImplementedError


def from_json(s):
    """Inverse of to_json: from_json(to_json(obj)) == obj, types intact."""
    raise NotImplementedError


def save(obj, path):
    """Write to_json(obj) to path (UTF-8)."""
    raise NotImplementedError


def load(path):
    """Read path and reconstruct the object."""
    raise NotImplementedError
