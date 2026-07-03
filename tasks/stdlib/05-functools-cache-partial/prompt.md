# Memoise and pre-bind

Two workhorses from `functools`: caching a pure function's results
(`lru_cache` / `cache`) and pre-binding arguments (`partial`). In
`solution.py`:

```python
def make_cached(fn):
    """Return a memoised version of `fn`.

    The returned callable takes the same positional arguments (all hashable)
    and returns the same results — but `fn` is invoked at most ONCE per
    distinct argument tuple; repeat calls are served from a cache.

    Each call to make_cached returns an independently-cached wrapper:
    make_cached(f) and make_cached(g) must not share entries.
    """

def int_parser(base):
    """Return a one-argument function that parses a string in the given base.

    int_parser(16)("ff") == 255. The intended one-liner is
    functools.partial(int, base=base).
    """

def fib(n):
    """The n-th Fibonacci number (fib(0) == 0, fib(1) == 1), recursively.

    Decorate/memoise it so that fib(200) returns instantly — naive
    exponential recursion will blow the grader's time budget.
    """
```

Examples:

```python
>>> calls = []
>>> def slow_double(x): calls.append(x); return 2 * x
>>> d = make_cached(slow_double)
>>> d(21), d(21), d(21)
(42, 42, 42)
>>> calls          # slow_double actually ran once
[21]
>>> int_parser(2)("101")
5
>>> fib(10)
55
```
