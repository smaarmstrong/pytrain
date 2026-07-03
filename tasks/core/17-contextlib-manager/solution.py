from contextlib import contextmanager

_MISSING = object()


@contextmanager
def patched(obj, name, value):
    old = getattr(obj, name, _MISSING)
    setattr(obj, name, value)
    try:
        yield obj
    finally:
        if old is _MISSING:
            delattr(obj, name)
        else:
            setattr(obj, name, old)


@contextmanager
def suppress_and_log(log, *exc_types):
    try:
        yield
    except exc_types as e:
        log.append(e)
