# FastAPI: dependency injection

In `solution.py`, build a FastAPI app (module-level `app`) for a small
product catalogue — but this time, wire shared machinery through
**`Depends`** instead of reaching for globals inside every endpoint.

Define at module level:

1. `STORE` — a plain dict mapping product name (`str`) to price (`float`).
   Starts empty.

2. `get_store()` — a dependency function returning the store the app
   should use. **Every endpoint must receive the store via
   `Depends(get_store)`** — the grader swaps the store with
   `app.dependency_overrides[get_store] = ...` and your endpoints must
   pick up the replacement. If any endpoint touches `STORE` directly,
   that test fails.

3. `list_params(q: str | None = None, limit: int = 5)` — one reusable
   dependency (a function or a class) providing the common query params
   for both GET endpoints below: `q` (optional substring filter on the
   product name, case-sensitive) and `limit` (max results, default 5).

Endpoints:

- `POST /products` — JSON body `{"name": str, "price": float}` (pydantic
  model, so bad bodies get 422). Puts the product into the injected
  store. Returns **201** `{"name": ..., "price": ...}`. A duplicate name:
  **409** `{"detail": "product exists"}`.

- `GET /products` — all products as a list of `{"name": ..., "price": ...}`
  sorted by **name** ascending, honouring `q` and `limit` from
  `list_params`.

- `GET /products/cheap` — same `q`/`limit` params via the *same*
  dependency, but only products with `price < 10`, sorted by **price**
  ascending (ties: by name).

Example:

```
POST /products {"name": "pen", "price": 1.5}   -> 201 {"name": "pen", "price": 1.5}
POST /products {"name": "pen", "price": 2.0}   -> 409 {"detail": "product exists"}
GET  /products?q=pe&limit=2                    -> 200 [{"name": "pen", ...}, ...]
GET  /products/cheap                           -> 200 [ ...price < 10, cheapest first... ]
```

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()`
at import time.
