# Pagination and filtering semantics

In `solution.py`, build a FastAPI application exposed as a module-level
variable named `app`. The dataset is fixed and provided in the starter — keep
it exactly as given (the grader relies on it):

```python
PRODUCTS = [
    {"id": i, "name": f"prod-{i:02d}", "category": ["dairy", "fruit", "veg"][i % 3],
     "price": round(0.5 * i, 2)}
    for i in range(1, 24)
]
```

One endpoint: `GET /products`, with query params

- `category: str` (optional) — keep only products whose `category` matches exactly
- `max_price: float` (optional) — keep only products with `price <= max_price`
- `page: int` — default `1`; values `< 1` must be rejected with **422**
- `page_size: int` — default `5`; values outside `1..20` must be rejected with **422**

Semantics (the point of the task — get these exactly right):

1. **Filter first, then paginate.** Both filters combine with AND. Preserve
   the original `PRODUCTS` order.
2. `total` is the number of products **after filtering** (not just the ones
   on this page).
3. `pages` is `ceil(total / page_size)` — `0` when nothing matches.
4. A `page` past the last one is **not** an error: respond 200 with an empty
   `items` list (and the correct `total`/`pages`).

Response body (200):

```json
{"items": [...], "total": 23, "page": 1, "page_size": 5, "pages": 5}
```

`items` holds the product dicts for that page, unchanged.

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()` at
import time.

Example session:

```
GET /products                          -> items = products 1..5, total 23, pages 5
GET /products?page=5                   -> items = products 21..23 (a short last page)
GET /products?category=fruit           -> total 8, pages 2
GET /products?category=fruit&max_price=5.0&page=2 -> filtered, then page 2 of that
GET /products?page=0                   -> 422
GET /products?page_size=50             -> 422
```
