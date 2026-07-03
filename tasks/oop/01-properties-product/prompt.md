# Product prices with properties

In `solution.py`, implement a class `Product`:

```python
class Product:
    currency = "GBP"          # class attribute, shared by all products

    def __init__(self, name, price=0.0): ...
```

Behaviour:

- `p.name` stores the name as given.
- `p.price` is a **property**:
  - the getter returns the current price as a `float` — ints passed in come
    back as floats (`Product("tea", 3).price == 3.0`, and it's a `float`);
  - the setter raises `ValueError` for a negative price. A failed set must
    leave the previous value untouched;
  - the deleter (`del p.price`) resets the price to `0.0` — the product
    stays usable and the price can be set again afterwards;
  - the constructor goes through the same validation: `Product("x", -5)`
    raises `ValueError`. Omitting `price` gives `0.0`.
- `currency` is a **class attribute** with default `"GBP"`:
  - reassigning `Product.currency = "EUR"` changes what every existing
    instance reports (unless it has its own instance attribute);
  - assigning `p.currency = "USD"` affects only that instance — other
    instances still see the class value.

Examples:

```python
>>> p = Product("tea", 2.5)
>>> p.price
2.5
>>> p.price = -1
ValueError: ...
>>> del p.price
>>> p.price
0.0
>>> Product.currency
'GBP'
```
