# Comprehension toolbox

Five small transformation functions in `solution.py`. Each is a natural
one-line comprehension (list, dict, set, nested, and a conditional
expression). Any correct implementation passes — but try to write each
as a single comprehension.

```python
def squares_of_evens(nums) -> list:
    """Squares of the even numbers, in original order.
    squares_of_evens([1, 2, 3, 4]) == [4, 16]."""

def word_lengths(words) -> dict:
    """{lowercased word: its length} for every non-empty word.
    Later duplicates (case-insensitively) overwrite earlier ones."""

def distinct_initials(names) -> set:
    """The set of uppercased first letters of the non-empty names.
    distinct_initials(["ada", "Alan", "grace", ""]) == {"A", "G"}."""

def flatten_matrix(matrix) -> list:
    """Row-major flattening of a list of rows.
    flatten_matrix([[1, 2], [3], []]) == [1, 2, 3]."""

def parity_labels(nums) -> list:
    """'even' or 'odd' for each number, same order.
    parity_labels([1, 2]) == ['odd', 'even']."""
```

Behaviour details:

- All functions accept any iterable of the stated element type and must
  not mutate their input.
- `word_lengths(["Hi", "there", "HI"])` → `{"hi": 2, "there": 5}`
  (length of the word as given — `"HI"` and `"hi"` have the same length,
  so overwriting is only observable through key order irrelevance).
- Empty input → empty list/dict/set of the right type.

Examples:

```python
>>> squares_of_evens(range(6))
[0, 4, 16]
>>> flatten_matrix([[1, 2], [3, 4]])
[1, 2, 3, 4]
>>> parity_labels([0, 7])
['even', 'odd']
```
