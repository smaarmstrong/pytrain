# Feel the GIL

The Global Interpreter Lock lets only one thread execute Python bytecode at
a time. Threads are great at overlapping *waiting*; for *CPU-bound* Python
they buy you nothing — but processes do. You'll build a tiny benchmark
harness that makes this measurable.

In `solution.py`, implement:

```python
def run_in_threads(fn, arg, n_workers):
    """Run fn(arg) once on EACH of n_workers threads, all started before
    any is joined (i.e. genuinely concurrent), wait for them all, and
    return the elapsed wall-clock seconds (float, time.monotonic)."""

def run_in_processes(fn, arg, n_workers):
    """Same, but each fn(arg) runs in its own worker PROCESS
    (multiprocessing.Process, a Pool, or ProcessPoolExecutor — your
    choice). Return elapsed wall-clock seconds. `fn` is picklable and
    importable."""

def gil_speedup(fn, arg, n_workers):
    """Return run_in_threads(...) / run_in_processes(...) — how many
    times faster processes are for this workload."""
```

Timing rules:

- Time the whole batch with `time.monotonic()`: start the clock, launch all
  workers, wait for all of them, stop the clock.
- Both functions must actually run the work concurrently. The grader
  checks this with a sleepy function first (4 workers sleeping 0.3s must
  finish in well under 1.2s), then hands you a CPU-burner and expects
  `gil_speedup` comfortably above 1 — the GIL made visible.

Example:

```python
>>> t = run_in_threads(some_cpu_burner, 2_000_000, 4)   # ~4x one call: serialized by the GIL
>>> p = run_in_processes(some_cpu_burner, 2_000_000, 4) # ~1x one call: true parallelism
>>> t / p
3.1  # varies with machine load — but well above 1
```
