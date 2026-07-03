# pandas: filter, sort, derive

In `solution.py` (with `import pandas as pd`), implement three functions.
Every function must return a **new** DataFrame — the input must never be
mutated (no new columns appearing on the caller's frame, no reordered rows).

The grader calls them with frames shaped like:

```python
pd.DataFrame({
    "product": ["anvil", "bolt", "cog", "dynamo", "elbow"],
    "qty":     [0,       120,    45,    3,        0],
    "price":   [99.5,    0.1,    2.5,   45.0,     1.25],
})
```

```python
def in_stock(df):
    """Only the rows with qty > 0, same columns, index RESET to 0..k-1."""

def top_n_by(df, col, n):
    """The n rows with the largest values in numeric column `col`,
    sorted descending by that column, index reset to 0..n-1.
    (Column values are distinct in the tests — no tie-breaking rules.)"""

def with_total(df):
    """A copy with an extra float column 'total' = qty * price.
    All original columns kept; 'total' added as the LAST column."""
```

Examples (with the frame above):

```python
>>> in_stock(df)["product"].tolist()
['bolt', 'cog', 'dynamo']
>>> top_n_by(df, "price", 2)["product"].tolist()
['anvil', 'dynamo']
>>> with_total(df)["total"].tolist()
[0.0, 12.0, 112.5, 135.0, 0.0]
```
