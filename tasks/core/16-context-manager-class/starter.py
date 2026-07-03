class Rollback:
    """Transactional edits to a dict: keep on success, restore on error.

    Implement __enter__ (snapshot + return the dict) and __exit__
    (restore on exception; return True only when swallowing).
    """

    def __init__(self, data: dict, swallow: bool = False):
        raise NotImplementedError
