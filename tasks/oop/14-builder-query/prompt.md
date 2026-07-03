# A fluent query builder

In `solution.py`, implement a fluent builder that assembles a SQL-ish
string step by step:

```python
class Query:
    def __init__(self, table): ...
    def select(self, *columns): ...
    def where(self, condition): ...
    def order_by(self, column, desc=False): ...
    def limit(self, n): ...
    def build(self): ...
```

Behaviour:

- `select`, `where`, `order_by` and `limit` each return a `Query`, so calls
  **chain** — and an intermediate result held in a variable can keep
  chaining.
- `build()` returns the query string, assembled from whatever was
  configured, in exactly this shape (single spaces, clauses in this order,
  absent clauses omitted entirely):

  `SELECT <columns> FROM <table> WHERE <conds> ORDER BY <col>[ DESC] LIMIT <n>`

  - *columns*: everything passed to `select(...)` across **all** calls, in
    order, joined by `", "`; if `select` was never called, use `*`;
  - *conds*: every `where(...)` condition, in call order, joined by
    `" AND "`;
  - *order by*: the **last** `order_by` call wins; append `" DESC"` when
    `desc=True`;
  - *limit*: `limit(n)` requires an `int` `n >= 0` — anything else
    (negative, float, string) raises `ValueError` immediately.
- `build()` does not consume the builder: calling it twice returns the same
  string.

Examples:

```python
>>> Query("users").build()
'SELECT * FROM users'
>>> (Query("users")
...     .select("id", "name")
...     .where("age >= 18").where("active = 1")
...     .order_by("name", desc=True)
...     .limit(10)
...     .build())
'SELECT id, name FROM users WHERE age >= 18 AND active = 1 ORDER BY name DESC LIMIT 10'
```
