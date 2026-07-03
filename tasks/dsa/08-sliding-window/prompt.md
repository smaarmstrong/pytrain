# Two pointers & sliding windows

In `solution.py`, implement:

```python
def max_window_sum(nums, k):
    """Return the maximum sum over all contiguous windows of exactly k
    elements.

    - k <= 0: raise ValueError.
    - k > len(nums): return None (no window of that size exists).
    - Negative numbers are allowed; the answer can be negative.
    - Technique: keep ONE running sum and slide (add the entering element,
      subtract the leaving one) — don't re-sum every window.
    """

def longest_unique_substring(s):
    """Return the LENGTH of the longest substring of s containing no
    repeated characters.

    - "" -> 0; "aaaa" -> 1; "abcabcbb" -> 3 ("abc").
    - Technique: two pointers (left/right) plus a set or last-seen dict.
    """

def pair_with_sum_sorted(nums, target):
    """nums is sorted ascending. Return a tuple (i, j), i < j, with
    nums[i] + nums[j] == target, or None. Use the converging two-pointer
    scan (one pointer at each end), not a nested loop.
    Any valid index pair is accepted."""
```

Examples:

```python
>>> max_window_sum([1, -2, 3, 4, -1], 2)
7                      # window [3, 4]
>>> max_window_sum([5], 3) is None
True
>>> longest_unique_substring("pwwkew")
3                      # "wke"
>>> pair_with_sum_sorted([1, 2, 4, 7, 11], 9)
(1, 3)                 # 2 + 7
>>> pair_with_sum_sorted([1, 2], 100) is None
True
```
