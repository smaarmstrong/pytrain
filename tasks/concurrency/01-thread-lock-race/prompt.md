# Guard the counter

A shared counter is exposed through a deliberately hostile interface: reading
it is *slow*, so the gap between "read the value" and "write it back" is wide
open for other threads to barge in. Your job is to make concurrent increments
safe with a `threading.Lock`.

The grader hands you a `probe` object with this interface:

```python
probe.read()      # -> current int value (slow: sleeps ~1ms internally)
probe.write(v)    # store v
```

In `solution.py`, implement:

```python
def increment_many(probe, lock, times):
    """Increment the probe `times` times.

    One increment is: read the current value, add 1, write it back.
    Each complete read-modify-write must be protected by `lock`
    (a threading.Lock) so concurrent callers never lose an update.
    """

def run_workers(probe, lock, n_threads, times_per_thread):
    """Spawn n_threads threading.Thread workers, each running
    increment_many(probe, lock, times_per_thread).

    Start them all, wait for them ALL to finish (join), then return the
    final counter value via probe.read().
    """
```

Requirements:

- `run_workers` must do the incrementing on `n_threads` **separate, new
  threads** — not the calling thread — and must not return until every
  worker has finished.
- With the lock held around each full read-modify-write, the final value is
  exactly `n_threads * times_per_thread`. If you lock only the read or only
  the write (or forget the lock), the slow probe makes threads overwrite
  each other and the count comes up short — the grader will catch it.

Example:

```python
lock = threading.Lock()
run_workers(probe, lock, n_threads=4, times_per_thread=10)  # -> 40
```
