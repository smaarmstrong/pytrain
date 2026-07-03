def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())
        return f"{type(self).__name__}({attrs})"

    cls.__repr__ = __repr__
    return cls


def singleton(cls):
    sentinel = object()
    instance = sentinel

    def get_instance(*args, **kwargs):
        nonlocal instance
        if instance is sentinel:
            instance = cls(*args, **kwargs)
        return instance

    return get_instance
