# Bounded: a validated-attribute descriptor

In `solution.py`, implement a reusable **descriptor** class:

```python
class Bounded:
    def __init__(self, minimum, maximum): ...
```

It is used as a class attribute to guard numeric fields:

```python
class Player:
    health = Bounded(0, 100)
    mana = Bounded(0, 50)

    def __init__(self, health, mana):
        self.health = health   # validated here too
        self.mana = mana
```

Behaviour (all validation happens **on assignment**, wherever it occurs —
in `__init__` or via plain `p.health = ...`):

- assigning a non-number (anything that is not `int`/`float`) raises
  `TypeError`;
- assigning a number outside `[minimum, maximum]` (inclusive at both ends)
  raises `ValueError`;
- a failed assignment leaves any previously stored value unchanged;
- valid values are stored **per instance**: two `Player`s hold independent
  values, and `health`/`mana` on the same instance don't interfere;
- reading the attribute before it has ever been assigned on that instance
  raises `AttributeError`;
- accessing the attribute on the *class* (`Player.health`) returns the
  `Bounded` descriptor object itself;
- the same `Bounded` class must work on any number of attributes and on
  several different owner classes at once (hint: `__set_name__`).

Examples:

```python
>>> p = Player(80, 20)
>>> p.health
80
>>> p.health = 150
ValueError: ...
>>> p.health = "full"
TypeError: ...
>>> p.health
80
```
