from contextlib import contextmanager  # the intended tool


def patched(obj, name, value):
    """Context manager: temporarily set obj.name = value, yield obj.

    Restore the old value on exit (remove the attribute if it did not
    exist before) — even when the block raises.
    """
    raise NotImplementedError


def suppress_and_log(log, *exc_types):
    """Context manager: suppress exceptions of the given types.

    Append the caught exception object to `log`; let anything else
    propagate.
    """
    raise NotImplementedError
