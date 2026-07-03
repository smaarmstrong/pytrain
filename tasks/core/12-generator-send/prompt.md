# Chunks and a running average

Two generator functions in `solution.py`.

## 1. `chunks(items, size)`

```python
def chunks(items, size):
    """Yield lists of up to `size` consecutive elements of `items`.

    - The final chunk may be shorter; no empty chunks are yielded.
    - LAZY: pull from `items` only as needed — asking for the first
      chunk must consume exactly `size` elements (or fewer at the end),
      and it must work on unbounded iterators.
    - size < 1 -> raise ValueError. (A generator function's body only
      runs at the first next(); the grader accepts the error raised at
      call time or on the first next() — whichever your design gives.)
    """
```

## 2. `averager()`

```python
def averager():
    """A generator you feed with .send().

    g = averager()
    next(g)          # prime it; this first yield produces None
    g.send(10)       # -> 10.0   (mean of [10])
    g.send(20)       # -> 15.0   (mean of [10, 20])
    g.send(4)        # -> 34/3   (mean of [10, 20, 4])

    Each send(x) returns the running mean as a float. State (count and
    total) lives in the generator's own local variables between sends.
    The generator never ends on its own; g.close() disposes of it.
    """
```

Notes:

- `chunks` must yield **lists** (fresh ones — mutating a yielded chunk
  must not affect later chunks).
- `averager` results are floats: `g.send(10)` is `10.0`.
- Independent `averager()` instances must not share state.

Examples:

```python
>>> list(chunks([1, 2, 3, 4, 5], 2))
[[1, 2], [3, 4], [5]]
>>> import itertools
>>> next(chunks(itertools.count(), 3))
[0, 1, 2]
>>> g = averager(); next(g)
>>> g.send(4), g.send(8)
(4.0, 6.0)
```
