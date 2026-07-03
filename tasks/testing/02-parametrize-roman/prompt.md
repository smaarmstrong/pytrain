# Roman numerals, table-driven

Your workspace contains `roman.py`:

```python
def to_roman(n): ...
```

Contract: for an integer `1 <= n <= 3999` it returns the Roman numeral as a
string, using standard subtractive notation (`4 -> "IV"`, `9 -> "IX"`,
`40 -> "XL"`, `90 -> "XC"`, `400 -> "CD"`, `900 -> "CM"`). Anything outside
`1..3999` raises `ValueError`.

## Your job

Write `test_roman.py` using `@pytest.mark.parametrize` — no copy-pasted
near-identical test functions.

1. A parametrized `test_to_roman` covering this table, with **exactly these
   test ids** (use `pytest.param(..., id=...)`):

   | id        | n    | expected      |
   |-----------|------|---------------|
   | `one`     | 1    | `"I"`         |
   | `four`    | 4    | `"IV"`        |
   | `nine`    | 9    | `"IX"`        |
   | `forty`   | 40   | `"XL"`        |
   | `ninety`  | 90   | `"XC"`        |
   | `mcmxciv` | 1994 | `"MCMXCIV"`   |
   | `max`     | 3999 | `"MMMCMXCIX"` |

2. The `one` and `max` cases (and only the range boundaries) additionally
   carry the mark `pytest.mark.boundary` — via
   `pytest.param(..., marks=pytest.mark.boundary)` — so that
   `pytest -m boundary` runs just those.

3. A parametrized test that `0`, `-1` and `4000` each raise `ValueError`.

## How it is graded

Your `test_roman.py` is copied — alone — next to one correct and several
buggy implementations of `roman.py`; it must pass the correct one and fail
every buggy one. The grader also collects your suite with `pytest
--collect-only` to check the required ids exist and that `-m boundary`
selects a strict, non-empty subset containing `one` and `max`.

Develop against the (correct) `roman.py` in your workspace:
`python -m pytest -q`.
