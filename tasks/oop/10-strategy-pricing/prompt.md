# Checkout with pluggable discount strategies

In `solution.py`, implement the strategy pattern: a checkout whose discount
behaviour is *injected*, never hard-coded.

```python
class Checkout:
    def __init__(self, strategy=None): ...
    def total(self, prices): ...

def no_discount(subtotal): ...
def percent_off(pct): ...
def bulk_discount(threshold, pct): ...
```

Behaviour:

- A *strategy* is any callable taking the subtotal (a float) and returning
  the discount amount to subtract.
- `Checkout(strategy)` stores it as `self.strategy`; with no argument it
  uses `no_discount`. The attribute is plain and reassignable — swapping
  `c.strategy = other` changes what subsequent `total()` calls do.
- `total(prices)` sums the price list, asks the current strategy for the
  discount, and returns `round(subtotal - discount, 2)`, floored at `0.0`
  (a discount larger than the subtotal never goes negative).
  `total([])` is `0.0`.
- Provided strategies:
  - `no_discount(subtotal)` returns `0`;
  - `percent_off(pct)` returns a **new strategy callable** giving
    `pct` percent off any subtotal;
  - `bulk_discount(threshold, pct)` returns a strategy giving `pct`
    percent off when `subtotal >= threshold`, otherwise nothing.

The grader also injects its own plain lambdas as strategies — your
`Checkout` must work with any callable, not just the three above.

Examples:

```python
>>> Checkout(percent_off(10)).total([6.0, 4.0])
9.0
>>> c = Checkout()
>>> c.total([10.0])
10.0
>>> c.strategy = bulk_discount(50, 20)
>>> c.total([60.0])
48.0
```
