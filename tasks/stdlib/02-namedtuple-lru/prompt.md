# Named tuples and an LRU sketch

Two classics from `collections`: a lightweight record type, and the
least-recently-used cache that `OrderedDict.move_to_end` (or plain dict
re-insertion) makes trivial. In `solution.py`:

## 1. `Track`

Create a record type with `collections.namedtuple`:

```python
Track = ...  # fields: title, artist, seconds (in that order)
```

It must behave like every namedtuple: instances are tuples, fields are
readable as attributes and by index, `Track._fields` is
`("title", "artist", "seconds")`, and `t._replace(seconds=200)` returns a
new modified instance.

## 2. `LRUCache`

```python
class LRUCache:
    def __init__(self, capacity):   # capacity >= 1
    def get(self, key):             # value, or None if absent; marks key as most recently used
    def put(self, key, value):      # insert or update; marks key as most recently used;
                                    # if len > capacity afterwards, evict the LEAST recently used key
    def keys(self):                 # list of keys, least- to most-recently used
    def __len__(self): ...
    def __contains__(self, key):    # membership test; must NOT affect recency
```

Rules:

- "Used" = touched by `get` (hit) or `put`. A `get` miss and `in` change nothing.
- Updating an existing key with `put` refreshes its recency (no eviction happens
  since the length didn't grow).

Example:

```python
>>> c = LRUCache(2)
>>> c.put("a", 1); c.put("b", 2)
>>> c.get("a")           # "a" is now most recent
1
>>> c.put("c", 3)        # evicts "b", the least recently used
>>> c.get("b") is None
True
>>> c.keys()
['a', 'c']
```
