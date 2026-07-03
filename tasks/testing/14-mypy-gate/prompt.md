# mypy as a quality gate

Your workspace `solution.py` contains four small report helpers that work
perfectly — and carry **zero type annotations**. Many teams gate merges on
exactly that: the code may run, but if the type checker isn't clean, CI is
red.

Your gate is:

```
python -m mypy --disallow-untyped-defs --disallow-incomplete-defs \
    --no-implicit-optional --warn-return-any solution.py
```

## Your job

Annotate every function — all parameters and every return type — until the
command above reports **no errors**, without changing any runtime behaviour:

- `mean(values)` — takes a list of floats, returns their arithmetic mean;
  raises `ValueError` on an empty list.
- `lookup(scores, name, default=None)` — `scores` maps `str` names to `int`
  scores; returns `scores[name]`, or `default` when the name is absent.
  Mind the default: `default` may be an `int` **or** `None`, and mypy with
  `--no-implicit-optional` will not infer that for you.
- `repeat(word, times=2)` — returns `word` repeated, space-separated.
- `first_long_word(words, min_len)` — the first word of at least `min_len`
  characters, or `None` if there isn't one. What does that make the return
  type?

Notes:

- Modern syntax is fine: `list[str]`, `dict[str, int]`, `int | None`.
- `--warn-return-any` is why lazy `Any` escapes won't help you: a function
  annotated to return a real type may not return an `Any` expression.
- Annotations only — the grader re-tests all runtime behaviour.

## How it is graded

The grader runs mypy with exactly the flags above on your `solution.py` and
requires exit code 0, then re-checks every function's behaviour.
