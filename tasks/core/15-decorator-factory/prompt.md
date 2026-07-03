# retry(times=...): a decorator factory

In `solution.py`, write a decorator WITH arguments — i.e. a function
that *returns* a decorator:

```python
def retry(times, exceptions=(ValueError,)):
    """@retry(3) / @retry(3, exceptions=(KeyError, OSError)).

    The decorated function is attempted up to `times` times in total.
    """
```

Behaviour of a function decorated with `@retry(times, exceptions=...)`:

- Call the original with the given args/kwargs. If it returns, return
  that value immediately (no further attempts).
- If it raises one of `exceptions`, try again — up to `times` total
  attempts. When the last attempt also raises a listed exception,
  let THAT exception propagate.
- An exception NOT listed in `exceptions` propagates immediately, with
  no further attempts (the grader counts attempts).
- `times=1` means exactly one attempt (no retries). `times < 1` →
  raise `ValueError` from the factory itself, at decoration time.
- No sleeping/backoff — retry immediately.
- Metadata: the decorated function keeps the original's `__name__`
  (use `functools.wraps` in the inner decorator).
- `exceptions` may be a single exception class or a tuple of them.

Example:

```python
attempts = []

@retry(3)
def flaky():
    attempts.append(1)
    if len(attempts) < 3:
        raise ValueError("not yet")
    return "ok"

>>> flaky()
'ok'
>>> len(attempts)
3
```
