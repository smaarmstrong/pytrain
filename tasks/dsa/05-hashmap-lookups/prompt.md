# Hash map workhorses

Three classic dict-powered problems. In `solution.py`, implement:

```python
def char_frequency(s):
    """Return a dict mapping each character of s to how many times it
    occurs. Empty string -> {}. Case-sensitive; spaces and punctuation
    count like any other character."""

def two_sum(nums, target):
    """Return a tuple (i, j) of two DIFFERENT indices with i < j and
    nums[i] + nums[j] == target, or None if no such pair exists.

    Any valid pair is accepted. The same *value* may be used twice if it
    appears at two indices — two_sum([3, 3], 6) == (0, 1) — but a single
    element can't pair with itself: two_sum([3], 6) is None.
    Use one pass with a dict of value -> index, not two nested loops.
    """

def group_anagrams(words):
    """Group words that are anagrams of each other (same letters, same
    counts; case-sensitive). Return a list of lists. Every input word
    appears in exactly one group; duplicates stay duplicated.
    Group order and order within groups don't matter."""
```

Edge cases the grader checks:

- `char_frequency("")` -> `{}`
- `two_sum([], 5)` and `two_sum([5], 5)` -> `None`
- negative numbers and zero targets in `two_sum`
- `group_anagrams([])` -> `[]`; a word with no partner forms its own group

Examples:

```python
>>> char_frequency("aab")
{'a': 2, 'b': 1}
>>> two_sum([2, 7, 11, 15], 9)
(0, 1)
>>> group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
[['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]   # any grouping order is fine
```
