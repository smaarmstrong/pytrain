# pandas: missing data & coercion

In `solution.py` (with `import pandas as pd`), implement four functions.
None of them may mutate the DataFrame they are given — always return a new
one (the grader checks).

```python
def missing_counts(df):
    """{column name: number of missing values} for every column, as plain
    ints. Columns with no missing values appear with 0."""

def fill_defaults(df, defaults):
    """Return a copy of df where missing values are filled per-column from
    the `defaults` dict, e.g. {"qty": 0, "grade": "?"}. Columns not named in
    `defaults` keep their NaNs."""

def drop_incomplete(df, required):
    """Return a copy containing only the rows that have a (non-missing)
    value in EVERY column named in the `required` list."""

def coerce_numeric(df, col):
    """Return a copy of df where column `col` (currently strings like
    "1.5", "2", "oops") is converted to a float dtype; unparseable entries
    become NaN."""
```

Example:

```python
>>> df = pd.DataFrame({"qty": [1.0, None], "grade": ["x", None]})
>>> missing_counts(df)
{'qty': 1, 'grade': 1}
>>> fill_defaults(df, {"qty": 0})["qty"].tolist()
[1.0, 0.0]
```
