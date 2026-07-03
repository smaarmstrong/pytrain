# 1-D dynamic programming: stairs & robbers

Two classics of the "answer for i depends on answers for i-1 and i-2"
pattern. Naive recursion recomputes the same subproblems exponentially many
times; memoise or (better) build the answers bottom-up in one pass.

In `solution.py`, implement:

```python
def climb_stairs(n):
    """How many distinct ways to climb a staircase of n steps, taking
    1 or 2 steps at a time.

    climb_stairs(0) == 1 (the empty climb), climb_stairs(1) == 1,
    climb_stairs(2) == 2 (1+1 or 2). n < 0: raise ValueError.

    Must be exact for n up to at least 300 — Python ints are fine with
    that; exponential recursion is not. (No timing trick here: the grader
    simply asks for n=300, which only finishes if you reuse subanswers.)
    """

def house_robber(loot):
    """`loot` is a list of non-negative ints, one per house along a
    street. Choose houses to rob maximising the total, but never rob two
    ADJACENT houses. Return the maximum total (0 for [] — rob nothing).

    house_robber([2, 7, 9, 3, 1]) == 12   # 2 + 9 + 1
    house_robber([2, 1, 1, 2]) == 4       # 2 + 2, skipping the middle
    Robbing nothing is allowed, so the answer is never negative.
    """
```

Requirements:

- `climb_stairs`: exact integer results (they get astronomically large);
  n up to 300 must return promptly.
- `house_robber`: lists up to length 3000 must return promptly;
  single-element and two-element lists work; zeros are legal loot.

Examples:

```python
>>> climb_stairs(4)
5
>>> climb_stairs(10)
89
>>> house_robber([1, 2, 3, 1])
4
>>> house_robber([])
0
```
