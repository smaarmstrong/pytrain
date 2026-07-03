# SQLAlchemy Core: tables & selects

In `solution.py`, using SQLAlchemy **Core** (2.x style — `sqlalchemy.create_engine`,
`Table`, `insert()`, `select()`; no ORM classes needed), implement four functions.

```python
def make_engine():
    """An Engine connected to an in-memory SQLite database."""

def build_schema(engine):
    """Create a 'products' table on that engine with columns:
      id    Integer, primary key
      name  String,  not nullable
      price Float,   not nullable
    Return the sqlalchemy Table object."""

def insert_rows(engine, table, rows):
    """Insert `rows` — a list of dicts like {"name": "anvil", "price": 9.5}
    (no ids; the primary key auto-generates) — and commit."""

def names_cheaper_than(engine, table, max_price):
    """The names of products with price < max_price, sorted alphabetically,
    as a plain list of str."""
```

Example:

```python
>>> eng = make_engine()
>>> tbl = build_schema(eng)
>>> insert_rows(eng, tbl, [{"name": "bolt", "price": 0.1}, {"name": "anvil", "price": 99.5}])
>>> names_cheaper_than(eng, tbl, 50.0)
['bolt']
```
