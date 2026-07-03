# Lint until clean: ruff without behaviour change

Your workspace `solution.py` contains three receipt helpers that **work
correctly** — every function returns exactly what it should — but running
the linter is another story:

```
python -m ruff check solution.py
```

reports a pile of violations from ruff's default rule set: merged imports
(`E401`), unused imports (`F401`), an import that isn't at the top of the
file (`E402`), comparisons to `None` and `True` (`E711`, `E712`), a bare
`except:` (`E722`), an f-string with nothing to format (`F541`) and an
unused local variable (`F841`).

## Your job

Fix `solution.py` until `ruff check` reports **zero** violations — while
changing **no behaviour at all**:

- `subtotal(prices)` still returns the sum of the prices (`0` for `[]`);
- `apply_discount(total, code)` still returns `total` for `code=None` or an
  unrecognised code, half for `"HALF"`, and `total * (100 - n) / 100` for a
  numeric string `"n"`;
- `summary(prices, code=None)` still returns the same `"TOTAL: ..."` string,
  floored to two decimal places.

Read each ruff message before fixing it — every rule here encodes a real
Python pitfall (why is `== None` suspect? what can a bare `except`
swallow?). `python -m ruff rule E712` explains a rule.
Fix by hand or with `--fix`; either way, re-run ruff until it prints
"All checks passed!".

## How it is graded

The grader runs `ruff check` (default rules) on your `solution.py` and
requires a clean exit, then re-tests all three functions' behaviour —
a refactor that lints clean but returns different values fails.
