# FastAPI: pydantic validators and nested models

In `solution.py`, build a FastAPI app (module-level `app`) with one
endpoint that leans on **pydantic v2** for all input checking: nested
models, `Field` constraints, a `field_validator` and a
`model_validator`. Your endpoint body should contain no validation `if`s
— anything invalid must already have been rejected with **422**.

## Models

- `Customer` — `name: str` (min length 1), `email: str` which must
  contain `"@"` (a `field_validator`; raise `ValueError` otherwise).

- `Item` — `sku: str` (min length 1), normalised to **uppercase** by a
  `field_validator`; `qty: int` with `qty >= 1`; `unit_price: float`
  with `unit_price > 0` (use `Field(ge=...)` / `Field(gt=...)`).

- `Order` — `customer: Customer`; `items: list[Item]` with **at least
  one item** (`Field(min_length=1)`); `coupon: str | None = None`,
  which must be `None`, `"SAVE10"` or `"SAVE20"` (validator; anything
  else raises `ValueError`).

## Endpoint

`POST /orders` — accepts an `Order`; returns status **201** with:

```json
{"customer": "<customer name>", "skus": ["<SKU1>", ...], "total": <float>}
```

- `skus` — the (uppercased) SKUs in the order, in input order.
- `total` — `sum(qty * unit_price)`, minus 10% for coupon `SAVE10` or
  20% for `SAVE20`, rounded to 2 decimal places with `round()`.

Example:

```
POST /orders {"customer": {"name": "Ada", "email": "ada@x.com"},
              "items": [{"sku": "pen-1", "qty": 3, "unit_price": 2.0}],
              "coupon": "SAVE10"}
  -> 201 {"customer": "Ada", "skus": ["PEN-1"], "total": 5.4}

POST /orders {..., "items": []}                 -> 422
POST /orders {..., "coupon": "HACK"}            -> 422
POST /orders {customer email without an @}      -> 422
POST /orders {an item with qty 0}               -> 422
```

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()`
at import time.
