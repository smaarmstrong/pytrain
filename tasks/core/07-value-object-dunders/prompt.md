# Card as a value object

In `solution.py`, write a `Card` class that behaves like a proper value
object: printable, comparable by value, and usable as a dict key /
set member.

```python
class Card:
    def __init__(self, rank: str, suit: str): ...
```

Required behaviour:

- **Attributes**: `card.rank` and `card.suit` hold the constructor args.
- **repr** — unambiguous, round-trippable style, exactly:
  `repr(Card('A', 'spades')) == "Card('A', 'spades')"`
  (use the `!r` of each attribute, so quoting adapts to the value).
- **str** — human-friendly, exactly:
  `str(Card('A', 'spades')) == 'A of spades'`.
  Note `print(card)` and `f"{card}"` use this, while a bare `card` at
  the REPL and containers (`print([card])`) use the repr.
- **Equality by value**: two Cards with equal rank and suit are `==`,
  regardless of identity. Comparing a Card with a non-Card (e.g. the
  tuple `('A', 'spades')`) is simply `False` — never an exception, and
  it must be False whichever operand comes first. (Return
  `NotImplemented` for foreign types rather than raising.)
- **Hashable, consistent with eq**: equal cards have equal hashes, so
  `{Card('A', 'spades'), Card('A', 'spades')}` has length 1, and a dict
  keyed by one instance can be read with another equal instance.
- Cards with the same rank but different suit (or vice versa) are not
  equal.

Examples:

```python
>>> c = Card('A', 'spades')
>>> c
Card('A', 'spades')
>>> print(c)
A of spades
>>> c == Card('A', 'spades'), c == Card('A', 'hearts'), c == ('A', 'spades')
(True, False, False)
>>> len({c, Card('A', 'spades'), Card('2', 'clubs')})
2
```
