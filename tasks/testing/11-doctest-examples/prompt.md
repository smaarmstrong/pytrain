# Docstrings that run

Your workspace `solution.py` contains three small, working functions whose
docstrings are prose only:

```python
def c_to_f(celsius): ...   # Celsius -> Fahrenheit
def clamp(value, lo, hi): ...  # clamp into [lo, hi]; lo > hi -> ValueError
def initials(name): ...    # "ada lovelace" -> "A.L."
```

## Your job

Turn each docstring into executable documentation: add **at least two
doctest examples per function** (lines starting with `>>>` followed by the
expected output). Every example must actually call the function it
documents, and every example must pass.

Tips:

- Check your work with `python -m doctest solution.py -v` — silence means
  "all passing" without `-v`.
- Mind float formatting: `c_to_f(0)` prints `32.0`, not `32`.
- An exception example must show the traceback in doctest form:

  ```
  >>> clamp(1, 5, 0)
  Traceback (most recent call last):
      ...
  ValueError: lo must not exceed hi
  ```

  (the `...` line skips the noisy stack.)

**Do not change what the functions do** — the grader re-tests their
behaviour. Only the docstrings gain examples.

## How it is graded

The grader runs your module's doctests with the `doctest` module: every
example must pass, each of the three functions must have at least two
examples that invoke it, and the functions must still behave exactly as
before.
