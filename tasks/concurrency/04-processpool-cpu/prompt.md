# Shipping work to other processes

Threads share one CPU-bound Python interpreter; processes don't. For
CPU-bound work you fan out to a `concurrent.futures.ProcessPoolExecutor` and
pay the price: everything crossing the boundary (the function AND its
arguments AND results) must be picklable, and the function must live in an
importable module.

In `solution.py`, implement:

```python
def process_map(fn, items, max_workers=4):
    """Apply fn to every item in worker PROCESSES via ProcessPoolExecutor.

    Return a list of results IN INPUT ORDER. `fn` is a picklable,
    importable function supplied by the caller (the grader passes things
    like math.factorial and its own module-level workers).
    """

def map_reduce(map_fn, reduce_fn, items, max_workers=4):
    """Map map_fn over items in worker processes (same rules as
    process_map), then combine in THIS process: return
    reduce_fn(list_of_results_in_input_order).

    e.g. map_reduce(math.factorial, sum, [1, 2, 3]) == 1 + 2 + 6 == 9
    """
```

Requirements:

- Work must actually run in separate worker processes — the grader passes a
  function that reports `os.getpid()` and expects to see more than one pid.
- Use the executor as a context manager so workers are cleaned up.
- `process_map` must handle an empty `items` list.

Example:

```python
>>> import math
>>> process_map(math.factorial, [5, 3, 0])
[120, 6, 1]
>>> map_reduce(math.factorial, max, [4, 2, 3])
24
```
