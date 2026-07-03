# CSV in, SQL out

The grader hands you a CSV file of sales with this exact header:

```
region,product,units,price
north,widget,10,2.50
south,gadget,3,10.00
```

`units` is an integer, `price` a float. In `solution.py`:

```python
def load_sales(csv_path):
    """Read the CSV with the `csv` module and load it into an in-memory
    SQLite database (sqlite3.connect(":memory:")).

    Create a table named `sales` with columns region (TEXT),
    product (TEXT), units (INTEGER), price (REAL) — properly typed, so
    SUM(units) etc. work numerically. Return the open Connection.
    """

def total_revenue(conn):
    """Sum of units * price over all rows, as a float. 0.0 for an empty
    table."""

def units_by_region(conn):
    """Dict mapping each region present to its total units,
    e.g. {"north": 17, "south": 3}."""

def top_product(conn):
    """The product name with the highest total revenue (units * price
    summed over its rows). Ties won't occur in the graded data."""
```

The query functions receive the connection returned by `load_sales` and
are expected to ask SQLite (they must also work on any other connection
with an equivalent `sales` table).

Example:

```python
>>> conn = load_sales("sales.csv")
>>> conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
2
>>> total_revenue(conn)
55.0
>>> top_product(conn)
'gadget'
```
