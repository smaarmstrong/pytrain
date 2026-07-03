# pandas: frames, dtypes, loc/iloc

In `solution.py` (with `import pandas as pd`), implement four functions.

```python
def make_inventory():
    """Build and return this exact DataFrame (default RangeIndex 0..3):

       sku     name  qty  price
    0   A1    anvil   10  99.50
    1   A2    apple   40   0.40
    2   B1     bolt  300   0.10
    3   B2  bracket   25   3.75

    Columns in exactly that order. `qty` must have an integer dtype and
    `price` a float dtype.
    """

def first_n_names(df, n):
    """The first n values of the 'name' column, as a plain Python list.
    (Positional — iloc/head territory.)"""

def row_by_sku(df, sku):
    """The single row whose 'sku' equals `sku`, as a plain dict like
    {"sku": "B1", "name": "bolt", "qty": 300, "price": 0.1}.
    Assume exactly one match exists."""

def numeric_summary(df):
    """{"total_qty": <sum of qty>, "max_price": <max of price>} for any
    DataFrame with the inventory columns."""
```

`first_n_names`, `row_by_sku` and `numeric_summary` are called with
DataFrames the grader builds itself (same columns, different data) — don't
assume the exact rows of `make_inventory`.

Example:

```python
>>> df = make_inventory()
>>> first_n_names(df, 2)
['anvil', 'apple']
>>> numeric_summary(df)["total_qty"]
375
```
