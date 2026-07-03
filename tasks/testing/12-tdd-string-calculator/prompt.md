# TDD kata: the string calculator

This task flips the usual arrangement one more time: **the tests are given,
the code is yours**. Your workspace contains `test_calc.py` — a complete,
currently-failing suite — and a stub `solution.py`.

Work TDD-style: run the suite, read the first failure, write just enough
code to fix it, repeat.

```
python -m pytest -q          # watch the reds turn green, one by one
```

## The contract (what the tests encode)

Implement in `solution.py`:

```python
def add(numbers): ...
```

- `numbers` is a string of integers; `add` returns their sum as an `int`.
- `add("") == 0`.
- By default, numbers are separated by commas and/or newlines, freely mixed:
  `add("1\n2,3") == 6`. Numbers may have several digits.
- A header line `//<char>\n` (e.g. `"//;\n1;2"`) declares a **custom
  single-character delimiter**: the rest of the string is separated by that
  character only. Any punctuation character may be used — including ones
  that are special in regular expressions, like `.` or `*`.
- Negative numbers are rejected: raise `ValueError` whose message is exactly
  `negatives not allowed: ` followed by all the negatives, in input order,
  joined by `", "` — e.g. `add("1,-2,3,-4")` raises
  `ValueError("negatives not allowed: -2, -4")`.

## How it is graded

The grader runs **its own copy of the given suite** against your
`solution.py` (so editing `test_calc.py` does not help), plus hidden
edge-case tests drawn from the contract above — multi-digit numbers,
newline-only input, regex-special custom delimiters, a lone negative,
negatives behind a custom delimiter. Make the given tests pass and honour
the whole contract and you're green.
