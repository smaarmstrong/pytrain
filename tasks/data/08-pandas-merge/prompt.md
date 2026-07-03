# pandas: merge, how=, concat

In `solution.py` (with `import pandas as pd`), implement three functions.

```python
def merge_sales(sales, products, how):
    """Merge `sales` and `products` on the shared 'product_id' column using
    the given join strategy (`how` is one of "inner", "left", "outer").

    `sales` has columns   product_id, units
    `products` has columns product_id, name

    Return the merged DataFrame. The usual merge semantics apply:
    - "inner": only product_ids present in BOTH frames
    - "left":  every sales row; missing product info becomes NaN
    - "outer": every product_id from either side; gaps become NaN
    """

def orders_with_names(orders, customers):
    """Left-merge on 'customer_id' so EVERY order is kept, in its original
    order, gaining the customer's 'name' (NaN when the customer is unknown).

    `orders` has columns   order_id, customer_id
    `customers` has columns customer_id, name
    """

def stack_frames(frames):
    """Concatenate a list of DataFrames (identical columns) vertically into
    one DataFrame with a fresh RangeIndex 0..n-1, rows in the given order."""
```

Don't mutate the inputs.

Example:

```python
>>> sales = pd.DataFrame({"product_id": [1, 4], "units": [5, 2]})
>>> products = pd.DataFrame({"product_id": [1, 3], "name": ["anvil", "clamp"]})
>>> merge_sales(sales, products, "inner")["product_id"].tolist()
[1]
>>> len(merge_sales(sales, products, "outer"))
3
```
