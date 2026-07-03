# Combinatorics without loops-of-loops

The combinatoric generators — `product`, `permutations`, `combinations` — and
`accumulate` replace whole families of nested loops. In `solution.py`:

```python
def dice_sums(n_dice, sides):
    """Distribution of sums when rolling `n_dice` fair dice with `sides` faces.

    Each die shows 1..sides. Return a dict mapping sum -> number of distinct
    rolls producing it (rolls are ordered: (1,2) and (2,1) are two rolls).
    n_dice >= 1.
    """

def unique_anagrams(word):
    """All distinct rearrangements of `word`, as a sorted list of strings.

    Repeated letters must not create duplicates: "aab" has 3 anagrams, not 6.
    """

def choose(items, k):
    """All k-element combinations of `items` as a list of tuples.

    Order within each tuple and between tuples follows the input order,
    exactly like itertools.combinations. k == 0 -> [()]; k > len(items) -> [].
    """

def running(values, op):
    """Cumulative reduction: [v0, op(v0, v1), op(op(v0, v1), v2), ...].

    `op` is a two-argument callable. Empty input -> [].
    """
```

Examples:

```python
>>> dice_sums(2, 6)[7]
6
>>> unique_anagrams("aab")
['aab', 'aba', 'baa']
>>> choose(["a", "b", "c"], 2)
[('a', 'b'), ('a', 'c'), ('b', 'c')]
>>> import operator
>>> running([1, 2, 3, 4], operator.add)
[1, 3, 6, 10]
>>> running([3, 1, 4, 1, 5], max)
[3, 3, 4, 4, 5]
```
