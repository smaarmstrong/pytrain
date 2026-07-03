# O(n) or bust

Both problems below have an obvious O(n²) solution and a classic O(n) one.
This task is graded WITH A CLOCK: correctness is checked on small inputs,
then each function runs on large inputs under a generous time budget. An
O(n) implementation finishes with seconds to spare; an O(n²) one will not
finish. That difference — not the clock itself — is the lesson.

In `solution.py`, implement:

```python
def max_subarray_sum(nums):
    """The maximum sum over all NON-EMPTY contiguous runs of `nums`.

    nums is a non-empty list of ints (positive and negative).
    max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6   # [4,-1,2,1]
    All-negative input: the best single element (the run can't be empty).

    O(n): one pass. Recomputing sums for every (start, end) pair is the
    O(n²) trap. The grader runs n = 500_000.
    """

def range_sums(nums, queries):
    """Answer many range-sum queries against one list.

    `queries` is a list of (lo, hi) pairs, 0 <= lo <= hi <= len(nums);
    each asks for sum(nums[lo:hi]) (half-open, so lo == hi -> 0).
    Return the list of answers, in query order.

    O(n + q): precompute prefix sums once, answer each query with one
    subtraction. Calling sum(nums[lo:hi]) per query is the O(n·q) trap.
    The grader runs n = 200_000 with 100_000 wide queries.
    """
```

Requirements:

- Exact ints; results must match a brute-force oracle on small inputs.
- The budgets are deliberately generous (many times the reference
  implementation's runtime) — only a change of complexity class blows
  them, never constant factors.

Examples:

```python
>>> max_subarray_sum([5, -9, 6, -2, 3])
7
>>> max_subarray_sum([-8, -3, -6])
-3
>>> range_sums([2, 4, 6, 8], [(0, 4), (1, 3), (2, 2)])
[20, 10, 0]
```
