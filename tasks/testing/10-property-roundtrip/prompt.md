# Seeded property test: RLE round-trip

Your workspace contains `codec.py`, a run-length encoder:

```python
def encode(s): ...    # "aaab" -> [("a", 3), ("b", 1)];  "" -> []
def decode(pairs): ...  # [("a", 3), ("b", 1)] -> "aaab"
```

Contract — for any string `s`:

1. **Round-trip**: `decode(encode(s)) == s`.
2. **Positive counts**: every `(char, count)` pair has `count >= 1`.
3. **Maximal runs**: adjacent pairs never repeat the same character —
   `encode("aaaa")` is `[("a", 4)]`, never `[("a", 2), ("a", 2)]`.

## Your job

Write `test_codec.py` containing:

1. A couple of small example tests (`""`, `"aaab"`, a decode call).
2. **One property-style test** that sweeps randomized inputs — seeded, so
   every run is identical:

   ```python
   rng = random.Random(1234)
   for _ in range(300):
       n = rng.randint(0, 40)
       s = "".join(rng.choice("ab") for _ in range(n))
       # assert all three invariants for s
   ```

   Use exactly this generator recipe (seed 1234, 300 strings, lengths 0–40,
   alphabet `"ab"`) and assert **all three invariants** on every generated
   string. The two-letter alphabet is deliberate: it makes empty strings,
   isolated characters and runs of 10+ all show up in the sample.

## How it is graded

Your `test_codec.py` is copied — alone — next to one correct and several
buggy implementations of `codec.py`. The bugs are the kind example tests
miss: one only misbehaves on runs of 10 or more, one drops a final
single-character run, one emits a zero-count pair for `""`, one never merges
runs at all. Hand-picked examples won't reliably hit those — the seeded
random sweep will. Your suite must pass the correct implementation and fail
every buggy one. Develop with `python -m pytest -q`.
