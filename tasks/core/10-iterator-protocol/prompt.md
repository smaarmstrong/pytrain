# Countdown, by the protocol

In `solution.py`, implement `Countdown` — an *iterable* (not an
iterator!) that counts from `start` down to 1.

```python
class Countdown:
    def __init__(self, start: int):
        """Counts start, start-1, ..., 2, 1. start <= 0 -> empty."""
```

The iterable/iterator distinction is the point of this task:

- `iter(countdown)` returns a NEW, independent iterator each time.
  So `list(c); list(c)` both give the full sequence, and two iterators
  advanced alternately don't interfere.
- Each iterator follows the protocol exactly:
  - `next(it)` yields the next value;
  - when exhausted it raises `StopIteration` — and KEEPS raising
    `StopIteration` on every subsequent `next()` (it must not restart);
  - `iter(it) is it` — an iterator is its own iterator (this is what
    lets a half-consumed iterator be used in a `for` loop).
- `Countdown(0)` and negative starts iterate zero times.
- The `Countdown` object itself must NOT be its own iterator (no
  `__next__` on the Countdown class — the grader checks that consuming
  it once doesn't exhaust it).

You may implement the iterator as a separate class with
`__iter__`/`__next__`, or make `Countdown.__iter__` a generator
function (generators satisfy the whole protocol automatically). Both
pass — the grader only checks behaviour.

Examples:

```python
>>> c = Countdown(3)
>>> list(c)
[3, 2, 1]
>>> list(c)          # re-iterable
[3, 2, 1]
>>> it = iter(c)
>>> next(it), next(it)
(3, 2)
>>> iter(it) is it
True
>>> next(it)
1
>>> next(it)
Traceback (most recent call last):
...
StopIteration
```
