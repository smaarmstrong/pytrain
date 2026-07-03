# Palindromes & run-length encoding

In `solution.py`, implement:

```python
def is_palindrome(s):
    """True if s reads the same forwards and backwards, considering ONLY
    alphanumeric characters and ignoring case.

    "A man, a plan, a canal: Panama" -> True
    "race a car"                     -> False
    ""    -> True (nothing to contradict)
    ".,!" -> True (no alphanumerics at all)
    """

def rle_encode(s):
    """Run-length encode: return a list of (char, run_length) tuples for
    each maximal run of consecutive equal characters, in order.

    "aaabcc" -> [("a", 3), ("b", 1), ("c", 2)]
    ""       -> []
    Any characters allowed, including digits and spaces.
    """

def rle_decode(pairs):
    """Inverse of rle_encode: [("a", 3), ("b", 1)] -> "aaab". [] -> ""."""
```

Requirements:

- `rle_decode(rle_encode(s)) == s` for every string.
- Runs are maximal: `rle_encode("aa a")` is `[("a", 2), (" ", 1), ("a", 1)]`,
  never two adjacent tuples with the same character.
- Use `str.isalnum()` / `str.lower()` (or casefold) for the palindrome
  cleaning — don't hardcode a punctuation list.

Examples:

```python
>>> is_palindrome("No 'x' in Nixon")
True
>>> rle_encode("aab")
[('a', 2), ('b', 1)]
>>> rle_decode([('x', 4)])
'xxxx'
```
