# polars: lazy frames

In `solution.py` (with `import polars as pl`), implement two functions over
a `pl.LazyFrame` with columns `category` (str), `qty` (int), `price` (float).

```python
def top_categories_query(lf, n):
    """BUILD (but do not run) the query:

    - keep only rows with qty > 0
    - per category, compute 'revenue' = sum of qty * price
    - sort by revenue descending
    - keep the first n rows

    Return the resulting *LazyFrame* — the whole point of lazy mode is that
    nothing executes until someone collects. Calling .collect() (or any
    other eager materialisation) inside this function is wrong: the grader
    checks the return value is still lazy.

    The result schema is two columns: 'category', 'revenue' (float).
    """

def top_categories(lf, n):
    """Run the same query and return the materialised pl.DataFrame."""
```

Because the query is built lazily, polars can optimise it (predicate and
projection pushdown) before anything executes — inspect it yourself with
`.explain()` if you're curious.

Example:

```python
>>> lf = pl.DataFrame({"category": ["a", "a", "b"], "qty": [2, 3, 5],
...                    "price": [1.0, 2.0, 3.0]}).lazy()
>>> top_categories(lf, 1).to_dicts()
[{'category': 'b', 'revenue': 15.0}]
>>> type(top_categories_query(lf, 1))
<class 'polars.lazyframe.frame.LazyFrame'>
```
