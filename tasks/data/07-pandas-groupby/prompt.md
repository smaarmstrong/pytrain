# pandas: groupby and named aggregations

In `solution.py` (with `import pandas as pd`), implement three functions.
The grader calls them with sales frames shaped like:

```python
pd.DataFrame({
    "region":  ["north", "north", "south", "south", "south", "east"],
    "product": ["a",     "b",     "a",     "b",     "c",     "a"],
    "units":   [10,      5,       8,       12,      1,       7],
    "revenue": [100.0,   50.0,    90.0,    140.0,   5.0,     70.0],
})
```

```python
def region_summary(df):
    """One row per region with NAMED aggregation columns, exactly:

    region | total_units (sum of units) | total_revenue (sum of revenue)
           | avg_units (mean of units)

    'region' is a normal column (not the index), rows sorted by region
    ascending, index reset to 0..k-1. Hint: df.groupby(...).agg(
    total_units=("units", "sum"), ...).
    """

def top_region(df):
    """The region name (str) with the highest total revenue."""

def product_units(df):
    """Plain dict mapping each product to its total units across all rows."""
```

Example (with the frame above):

```python
>>> region_summary(df)
  region  total_units  total_revenue  avg_units
0   east            7           70.0        7.0
1  north           15          150.0        7.5
2  south           21          235.0        7.0
>>> top_region(df)
'south'
>>> product_units(df)
{'a': 25, 'b': 17, 'c': 1}
```
