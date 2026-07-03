# Approximately equal: floats and collections

Your workspace contains `stats.py`:

```python
def mean(xs): ...       # arithmetic mean
def variance(xs): ...   # POPULATION variance (divide by n, not n-1)
def normalize(xs): ...  # list of xs[i] / sum(xs)
```

- `mean([])` and `variance([])` raise `ValueError`.
- `normalize(xs)` raises `ValueError` when `sum(xs) == 0`.
- `variance([x])` is `0.0`.

Examples (note the `≈`!):

```python
mean([0.1, 0.1, 0.1])            # ≈ 0.1
variance([0.1, 0.2, 0.3, 0.4])   # ≈ 0.0125
normalize([1.0, 2.0, 3.0])       # ≈ [1/6, 1/3, 1/2]  (sums to ≈ 1.0)
```

**The contract only guarantees results to within 1e-6 relative accuracy.**
Different correct implementations sum in different orders (`sum` vs
`math.fsum`, one-pass vs two-pass variance) and disagree in the last few
bits — `mean([0.1, 0.1, 0.1]) == 0.1` is `False` in some of them. Exact
`==` on floats is a bug in *your tests*.

## Your job

Write `test_stats.py` covering all three functions — typical values, the
documented examples above, the error cases, and `normalize`'s output as a
whole collection (`pytest.approx` accepts lists). Use `pytest.approx`
everywhere a float comes back.

## How it is graded

Your `test_stats.py` is copied — alone — next to **two different correct
implementations** (it must pass BOTH — this is where exact float equality
dies) and several buggy ones (sample instead of population variance,
normalizing by max instead of sum, dropped data, missing error cases — all
wrong by far more than 1e-6). It must fail every buggy one. Keep everything
in `test_stats.py`; develop with `python -m pytest -q`.
