"""Persistence layer: load/save the JSON task list (suggested split)."""


def load(path):
    """Return the list of task dicts stored at `path`; [] if the file is missing."""
    raise NotImplementedError


def save(path, tasks):
    """Write the task list to `path` as a JSON array."""
    raise NotImplementedError
