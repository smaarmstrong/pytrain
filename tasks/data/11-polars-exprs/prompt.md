# polars: expressions

In `solution.py` (with `import polars as pl`), implement four functions.
Each receives a `pl.DataFrame` with columns `item` (str), `category` (str),
`qty` (int), `price` (float) and must return a `pl.DataFrame`. Use polars
expressions (`pl.col(...)`) — pandas is not installed in this task's venv.

```python
def select_cols(df, cols):
    """Only the named columns, in the given order."""

def filter_at_least(df, min_qty):
    """Only the rows with qty >= min_qty (original row order kept)."""

def add_revenue(df):
    """All original columns plus a new float column 'revenue' = qty * price."""

def category_totals(df):
    """One row per category with columns 'category' and 'total_qty'
    (the sum of qty), sorted by category ascending."""
```

Example:

```python
>>> df = pl.DataFrame({"item": ["anvil", "bolt"], "category": ["tools", "parts"],
...                    "qty": [2, 100], "price": [99.5, 0.1]})
>>> add_revenue(df)["revenue"].to_list()
[199.0, 10.0]
>>> category_totals(df).to_dicts()
[{'category': 'parts', 'total_qty': 100}, {'category': 'tools', 'total_qty': 2}]
```
