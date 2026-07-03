# Delegation with yield from

`yield from sub` does two things a plain `for x in sub: yield x` loop
does not teach you: it delegates the *whole* generator protocol to the
subiterator, and — the part this task focuses on — it evaluates to the
subgenerator's **return value**. A generator's `return x` travels out
as `StopIteration(x)`; the caller can read it as the exception's
`.value`, and a delegating generator receives it as the result of the
`yield from` expression.

Implement three generator functions in `solution.py`:

```python
def flatten(items):
    """Lazily yield the leaves of arbitrarily nested lists/tuples."""

def chunk_sum(chunk):
    """Yield each number in `chunk`; RETURN their sum."""

def stream_sums(chunks):
    """Yield every number of every chunk; RETURN the per-chunk sums."""
```

## `flatten(items)`

- `items` is any iterable whose elements are either leaves or nested
  `list`/`tuple` structures of arbitrary depth. Yield the leaves
  left-to-right. Anything that is not a `list` or `tuple` is a leaf —
  in particular strings are yielded whole, never iterated into.
- Must return a lazy iterator: calling `flatten(...)` consumes nothing,
  and each `next()` pulls from `items` only as needed. (The grader
  feeds it a source that blows up if read too far.)

## `chunk_sum(chunk)`

- `chunk` is an iterable of numbers. Yield each one in order, then
  finish with the total as the generator's return value: exhausting it
  raises `StopIteration` whose `.value` is the sum (`0` for an empty
  chunk, which yields nothing).

## `stream_sums(chunks)`

- `chunks` is an iterable of chunks. Yield all numbers of chunk 0, then
  chunk 1, ... (delegation with `yield from chunk_sum(...)` is the
  intended shape), and return a list with each chunk's sum, in order.
  For no chunks, return `[]`.

Examples:

```python
>>> list(flatten([1, [2, [3, 4]], 5]))
[1, 2, 3, 4, 5]

>>> g = chunk_sum([4, 5])
>>> next(g), next(g)
(4, 5)
>>> try:
...     next(g)
... except StopIteration as e:
...     e.value
9

>>> g = stream_sums([[1, 2], [3]])
>>> list(g)          # the yields
[1, 2, 3]
>>> # a fresh run, reading the return value this time:
>>> g = stream_sums([[1, 2], [3]])
>>> try:
...     while True: next(g)
... except StopIteration as e:
...     e.value
[3, 3]
```
