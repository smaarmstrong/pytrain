# Pools and pickles

`multiprocessing.Pool` moves work between processes by **pickling** it: the
function, its arguments and its results all travel through pipes as pickled
bytes. That's why a lambda or an open file handle blows up the moment you
try to send it to a worker.

In `solution.py`, implement:

```python
def pool_map(fn, items, processes=4):
    """Apply fn to every item using a multiprocessing.Pool of `processes`
    workers. Return the results IN INPUT ORDER.

    Use the pool as a context manager (or close/join it) so no worker
    processes are left behind. `fn` must be picklable — if it isn't,
    let the pickling error propagate to the caller.
    """

def is_picklable(obj):
    """Return True if pickle.dumps(obj) succeeds, False if it raises
    ANY exception (PicklingError, TypeError, AttributeError...)."""

def split_picklable(objs):
    """Partition objs into (picklable, unpicklable) — two lists that
    preserve the original relative order. Uses the same test as
    is_picklable."""
```

Requirements:

- `pool_map` really distributes work: the grader sends jobs that report
  their `os.getpid()` and expects more than one worker pid.
- `pool_map` with a lambda must raise (that's the pickling lesson — don't
  catch it).
- `split_picklable` compares by identity/position, not equality: the exact
  objects go into the two lists.

Example:

```python
>>> pool_map(math.factorial, [4, 2])
[24, 2]
>>> is_picklable(lambda x: x)
False
>>> split_picklable([1, print, "hi"])   # print pickles fine; a lambda wouldn't
([1, print, 'hi'], [])
```
