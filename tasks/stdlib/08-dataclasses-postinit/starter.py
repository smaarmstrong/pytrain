class Rectangle:
    """Dataclass: width, height; derived .area; ValueError on non-positive."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class User:
    """Dataclass: name + InitVar password -> stores only password_hash."""

    def __init__(self, *args, **kwargs):
        raise NotImplementedError


def check(user, attempt):
    """True iff `attempt` is the password `user` was constructed with."""
    raise NotImplementedError
