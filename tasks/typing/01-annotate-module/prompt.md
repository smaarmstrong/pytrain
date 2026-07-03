# Annotate the config helpers

Your `solution.py` already contains four small, **working** config helpers —
but not a single type annotation. Annotate the module fully. Do **not** change
what the functions do: the grader checks behaviour first, then runs

```
mypy --disallow-untyped-defs --disallow-incomplete-defs solution.py
```

and requires zero errors.

The intended types (annotate exactly this contract; spell unions either as
`X | None` or `Optional[X]`, both are accepted):

```python
def parse_port(value: str) -> int | None:
    """int port for a numeric string in 0..65535, else None."""

def normalize_host(host: str | None) -> str:
    """Lower-cased, stripped host; 'localhost' when None or blank."""

def get_flag(settings: dict[str, str], name: str, default: bool = False) -> bool:
    """True iff settings[name] is one of '1'/'true'/'yes'/'on' (any case);
    `default` when the key is missing."""

def summarize(settings: dict[str, str]) -> str:
    """'key=value' pairs, sorted by key, joined with ', '."""
```

Examples:

```python
>>> parse_port(" 443 ")
443
>>> parse_port("70000") is None
True
>>> normalize_host(None)
'localhost'
>>> summarize({"b": "2", "a": "1"})
'a=1, b=2'
```

The grader also inspects `typing.get_type_hints` on your functions, so the
`None`-unions must really be there (e.g. `parse_port` must be declared to
return an int-or-None union, not just `int`).
