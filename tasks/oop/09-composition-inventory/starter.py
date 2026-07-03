class Inventory:
    """A container that WRAPS a list (composition) and records a history of
    successful mutations. Must not inherit from list — see prompt.md."""

    def __init__(self, items=None):
        raise NotImplementedError
