# Config errors, chained

In `solution.py`, build a small exception hierarchy and two functions
that use it.

```python
class ConfigError(Exception): ...
class MissingKeyError(ConfigError): ...      # a key was absent
class InvalidValueError(ConfigError): ...    # a value failed to parse
```

Both subclasses must be catchable as `ConfigError`.

```python
def parse_port(raw) -> int:
    """Convert `raw` to an int port number.

    - Non-integer input (e.g. "abc"): raise InvalidValueError, CHAINED
      from the original ValueError with `raise ... from` — the grader
      inspects `err.__cause__`.
    - Integer out of range (not 1..65535): raise InvalidValueError
      (no chaining required).
    - Valid: return the int. parse_port("8080") == 8080.
    """

def get_port(config: dict, log: list) -> int:
    """Look up config["port"], parse it with parse_port, and record an
    audit trail in `log` (append strings, in this order):

    - If "port" is missing: append "missing", then raise MissingKeyError.
    - If parse_port raises: append "invalid", re-raise the same exception.
    - ONLY if everything succeeded: append "ok" (use try/except/else —
      "ok" must not be appended when an error occurs after the lookup).
    - In ALL cases (success or any failure) the LAST entry appended must
      be "done" (use finally).

    Success -> log ends ["ok", "done"] and the parsed port is returned.
    """
```

Examples:

```python
>>> parse_port("443")
443
>>> try:
...     parse_port("abc")
... except InvalidValueError as e:
...     isinstance(e.__cause__, ValueError)
True
>>> log = []
>>> get_port({"port": "80"}, log)
80
>>> log
['ok', 'done']
>>> log = []
>>> get_port({}, log)   # raises MissingKeyError
>>> log
['missing', 'done']
```
