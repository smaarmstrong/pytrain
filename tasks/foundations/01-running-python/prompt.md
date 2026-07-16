# Run a Python file

Turn `solution.py` into a script that, when run with `python3 solution.py`,
prints exactly these two lines and nothing else:

```
hello from pytrain
the answer is 42
```

Behaviour details:

- Two lines of output, each ending in a newline. No extra blank lines,
  no extra spaces.
- The `42` on the second line must be **computed** by Python (for example
  `6 * 7`) and placed into the text — don't just type the digits into the
  string. The grader can only see the output, but doing the arithmetic is
  the point of the exercise: a script line can contain any expression.
- The script must exit normally (no errors).

Try it yourself before grading: from the repo root run

```
python3 workspace/foundations/01-running-python/solution.py
```

and check the two lines appear. Then grade it with `check`.
