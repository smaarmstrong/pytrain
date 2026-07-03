# Stream surgery with itertools

`itertools` works on *streams*: every function here must accept any iterable
— including one-shot generators and **infinite** ones where noted — and must
not materialise more of the input than needed. In `solution.py`:

```python
def take(iterable, n):
    """The first n items, as a list.

    Must work on INFINITE iterables (e.g. itertools.count()) — so no
    list(iterable) allowed. Fewer than n items -> all of them. n == 0 -> [].
    """

def flatten(iterables):
    """One level of flattening: chain all inner iterables into one list.

    Inner iterables may be one-shot generators. flatten([]) -> [].
    """

def runs(iterable):
    """Run-length encode consecutive equal values.

    Return a list of (value, count) tuples for each maximal run of equal
    consecutive items. Works on strings too. Empty input -> [].
    """

def deltas(iterable):
    """Differences between consecutive items, as a list.

    Fewer than two items -> []. Single pass over a one-shot iterable.
    """
```

Examples:

```python
>>> import itertools
>>> take(itertools.count(10), 3)
[10, 11, 12]
>>> flatten([[1, 2], (), iter([3])])
[1, 2, 3]
>>> runs("aaabbc")
[('a', 3), ('b', 2), ('c', 1)]
>>> deltas([3, 7, 2])
[4, -5]
```

The intended tools are `itertools.islice`, `itertools.chain` (or
`chain.from_iterable`), `itertools.groupby`, and `itertools.pairwise` — but
any implementation with the same behaviour passes.
