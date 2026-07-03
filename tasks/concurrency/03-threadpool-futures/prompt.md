# Futures three ways

`concurrent.futures.ThreadPoolExecutor` gives you three idioms: `.map` for
ordered bulk work, `.submit` for individual futures, and `as_completed` to
react to whichever finishes first. Use all three.

In `solution.py`, implement:

```python
def parallel_map(fn, items, max_workers):
    """Apply fn to every item using a ThreadPoolExecutor.

    Return a list of results IN INPUT ORDER. If any call raises, let the
    exception propagate to the caller (executor.map already behaves
    this way).
    """

def try_map(fn, items, max_workers):
    """Like parallel_map, but capture failures instead of raising.

    Submit each call individually; as each future completes, record its
    outcome. Return a dict mapping each item to a tuple:
        ("ok", result)                       if the call succeeded
        ("error", type(exc).__name__)        if it raised
    Items are hashable and unique.
    """

def first_result(fn, items, max_workers):
    """Run fn over all items concurrently and return the RESULT of
    whichever call completes FIRST (use as_completed). Don't wait for
    the rest before returning."""
```

Requirements:

- All three must actually run calls concurrently (the grader uses sleepy
  functions and a stopwatch).
- Use the executor as a context manager or otherwise clean up sensibly.

Examples:

```python
>>> parallel_map(str.upper, ["a", "b"], 2)
['A', 'B']
>>> try_map(lambda x: 1 // x, [1, 0], 2)
{1: ('ok', 1), 0: ('error', 'ZeroDivisionError')}
```
