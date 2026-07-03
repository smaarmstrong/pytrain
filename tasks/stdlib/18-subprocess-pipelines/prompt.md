# Child processes, captured and chained

Run other programs from Python with `subprocess`. To stay
cross-platform, the only program you run is **Python itself**: commands
are Python source strings executed as `[sys.executable, "-c", code]`.
In `solution.py`:

```python
def run_code(code):
    """Run `code` in a fresh Python subprocess, capturing its output.

    Return a tuple (stdout, stderr, returncode) with the two streams as
    text (str, not bytes). Never raise on a non-zero exit.
    """

def checked_output(code):
    """Run `code` and return its stdout as text — but if the subprocess
    exits non-zero, raise subprocess.CalledProcessError (the behaviour
    check=True gives you)."""

def pipeline(code1, code2):
    """A two-stage pipeline, like `python -c code1 | python -c code2` in
    a shell (but WITHOUT using a shell):

    run `code1`, feed its stdout into `code2`'s STDIN, and return
    `code2`'s stdout as text. The second stage reads sys.stdin.
    """
```

Examples:

```python
>>> run_code("print(21 * 2)")
('42\n', '', 0)
>>> out, err, rc = run_code("import sys; sys.exit(3)")
>>> rc
3
>>> checked_output("print('ok')")
'ok\n'
>>> checked_output("raise SystemExit(1)")   # raises CalledProcessError
>>> pipeline("print('3\\n1\\n2')",
...          "import sys; print(sum(int(l) for l in sys.stdin))")
'6\n'
```
