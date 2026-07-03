from typing import Protocol, runtime_checkable  # noqa: F401

# Define the Drawable protocol here (see prompt.md).


def draw_all(items):
    """Validate every item is Drawable first, then return their draw() outputs."""
    raise NotImplementedError
