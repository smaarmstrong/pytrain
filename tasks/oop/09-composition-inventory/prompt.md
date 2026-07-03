# Inventory by composition

In `solution.py`, implement a container that *wraps* a list instead of
inheriting from it:

```python
class Inventory:
    def __init__(self, items=None): ...
```

Behaviour:

- **Composition, not inheritance**: `isinstance(Inventory(), list)` must be
  `False`. Keep the underlying list as an internal attribute and delegate
  to it.
- `Inventory(items)` copies the optional initial iterable — mutating the
  original list afterwards must not affect the inventory.
- `inv.add(item)` appends an item.
- `inv.remove(item)` removes the first occurrence; a missing item raises
  `ValueError` (delegation makes this free).
- Delegated container behaviour, preserving insertion order:
  - `len(inv)`;
  - `item in inv`;
  - `inv[i]` — indexing, out-of-range raises `IndexError`;
  - `for x in inv` — iteration.
- `inv.history` is a list of tuples recording every **successful** mutation
  in order: `("add", item)` or `("remove", item)`. Constructor items are
  not recorded, and a failed `remove` records nothing.

Examples:

```python
>>> inv = Inventory(["axe"])
>>> inv.add("rope"); inv.remove("axe")
>>> list(inv), len(inv), "rope" in inv
(['rope'], 1, True)
>>> inv.history
[('add', 'rope'), ('remove', 'axe')]
```
