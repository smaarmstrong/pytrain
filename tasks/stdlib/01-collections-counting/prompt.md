# Counting, grouping, tailing

The `collections` module has purpose-built containers for the three most
common "bookkeeping" jobs: counting (`Counter`), grouping (`defaultdict`),
and bounded history (`deque`). In `solution.py`, implement:

```python
def word_counts(text):
    """Case-insensitive word frequencies.

    Split `text` on whitespace, lowercase each word, and return a mapping
    word -> count. Empty text -> empty mapping.
    """

def top_n(text, n):
    """The n most common words of `text` as a list of (word, count) tuples.

    Words as in word_counts. Sort by count descending; break ties
    alphabetically (ascending). If there are fewer than n distinct words,
    return them all.
    """

def group_by_length(words):
    """Group a list of strings by their length.

    Return a dict mapping length -> list of words of that length, each list
    preserving the original input order.
    """

def tail(iterable, n):
    """The last n items of any iterable, as a list.

    `iterable` may be a one-shot generator and may be huge — do not build a
    full list of it. Fewer than n items -> return them all. n == 0 -> [].
    """
```

Examples:

```python
>>> word_counts("The cat saw the dog")
{'the': 2, 'cat': 1, 'saw': 1, 'dog': 1}
>>> top_n("b b a a c", 2)
[('a', 2), ('b', 2)]
>>> group_by_length(["hi", "the", "a", "an"])
{2: ['hi', 'an'], 3: ['the'], 1: ['a']}
>>> tail(iter(range(1000)), 3)
[997, 998, 999]
```
