# Temperature: alternative constructors

In `solution.py`, implement a class `Temperature`:

```python
class Temperature:
    def __init__(self, celsius): ...
```

Behaviour:

- `Temperature(c)` stores `t.celsius` as a `float`. Temperatures below
  absolute zero (`-273.15`) raise `ValueError`.
- `Temperature.from_fahrenheit(f)` — a **classmethod** returning a new
  instance with `celsius = (f - 32) * 5 / 9`.
- `Temperature.from_string(text)` — a **classmethod** parsing strings like
  `"21.5C"`, `"-40c"`, `"70.7F"`, `"32f"`: a number followed by a one-letter
  unit suffix, `C`/`F`, case-insensitive. Fahrenheit values are converted to
  celsius. Anything unparsable (`"21.5K"`, `"abcC"`, `""`) raises
  `ValueError`.
- `Temperature.is_valid(celsius)` — a **staticmethod** returning `True` iff
  `celsius >= -273.15`. Callable on the class without an instance.
- Both classmethods must build the instance via `cls(...)`, so a subclass
  `class Freezer(Temperature): pass` gets `Freezer` instances back from
  `Freezer.from_fahrenheit(32)` and `Freezer.from_string("1C")`.

Examples:

```python
>>> Temperature.from_fahrenheit(212).celsius
100.0
>>> Temperature.from_string("70.7f").celsius
21.5
>>> Temperature.is_valid(-300)
False
```
