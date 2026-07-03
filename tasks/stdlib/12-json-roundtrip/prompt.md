# JSON beyond the basic types

JSON has no `set` and no dates — `json.dumps` raises `TypeError` on both.
The escape hatch is a custom encoder (`default=`/`JSONEncoder`) paired
with an `object_hook` that recognises your markers on the way back in.
In `solution.py`:

```python
def to_json(obj):
    """Serialise `obj` to a JSON string.

    `obj` is built from: dict (string keys), list, str, int, float, bool,
    None — plus `set` and `datetime.date`, nested anywhere. The result
    must be VALID JSON (parseable by a plain json.loads); how you encode
    sets/dates inside it is up to you, as long as from_json undoes it.
    """

def from_json(s):
    """Parse a string produced by to_json, reconstructing set and
    datetime.date objects exactly. For any supported obj:

        from_json(to_json(obj)) == obj

    with types preserved (a set comes back as a set, not a list; a date
    as datetime.date, not str).
    """

def save(obj, path):
    """Write to_json(obj) to `path` (UTF-8)."""

def load(path):
    """Read `path` and return the reconstructed object."""
```

Plain data must stay plain: `from_json(to_json({"a": [1, 2]}))` is just
`{"a": [1, 2]}`, and `to_json` of pure-JSON data must be loadable by any
JSON consumer as those same values.

Example:

```python
>>> import datetime
>>> team = {"name": "core", "tags": {"py", "web"},
...         "since": datetime.date(2021, 9, 1)}
>>> from_json(to_json(team)) == team
True
>>> save(team, p); load(p) == team
True
```
