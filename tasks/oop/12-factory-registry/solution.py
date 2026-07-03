_registry = {}


def register(name):
    def decorator(cls):
        if name in _registry:
            raise ValueError(f"{name!r} is already registered")
        _registry[name] = cls
        return cls
    return decorator


def create(name, *args, **kwargs):
    try:
        cls = _registry[name]
    except KeyError:
        raise ValueError(f"no plugin registered under {name!r}") from None
    return cls(*args, **kwargs)


def registered_names():
    return sorted(_registry)
