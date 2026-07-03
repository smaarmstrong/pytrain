# Self-returning builders and __init_subclass__

Annotating chainable methods as returning the class name breaks subclassing:
a subclass's `.where(...)` would be typed as returning the base class.
`typing.Self` fixes that. And `__init_subclass__` lets a base class react
every time it is subclassed. In `solution.py`:

1. A chainable query builder whose chain methods are annotated `-> Self`
   and `return self` (the same instance, so subclass chains stay subclassed):

```python
class QueryBuilder:
    def __init__(self, table: str) -> None: ...

    def where(self, cond: str) -> Self:
        """Add a condition; return self."""

    def limit(self, n: int) -> Self:
        """Set/replace the limit; return self."""

    def build(self) -> str:
        """'SELECT * FROM <table>'
        + ' WHERE <cond1> AND <cond2>...'  (in insertion order, if any)
        + ' LIMIT <n>'                      (if set)"""
```

2. A plugin base that registers every subclass:

```python
class Plugin:
    registry: ClassVar[dict[str, type]] = {}

    def __init_subclass__(cls, *, name: str | None = None, **kwargs: Any) -> None:
        """Register cls in Plugin.registry under `name`, or under
        cls.__name__.lower() when no name keyword is given.
        MUST call super().__init_subclass__(**kwargs) so cooperative
        bases still run."""
```

Examples:

```python
>>> QueryBuilder("users").where("age > 21").where("active").limit(10).build()
'SELECT * FROM users WHERE age > 21 AND active LIMIT 10'
>>> QueryBuilder("users").build()
'SELECT * FROM users'

>>> class CsvLoader(Plugin): ...
>>> class JsonLoader(Plugin, name="json"): ...
>>> Plugin.registry["csvloader"] is CsvLoader and Plugin.registry["json"] is JsonLoader
True
```

The grader checks the resolved return annotation of `where`/`limit` is
`typing.Self`, that chaining a `QueryBuilder` *subclass* yields that subclass,
and that `super().__init_subclass__(**kwargs)` really is called (it mixes in
another base with its own `__init_subclass__`).
