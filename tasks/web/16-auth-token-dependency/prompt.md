# Auth: token check as a reusable dependency

In `solution.py`, build a FastAPI application exposed as a module-level
variable named `app`. Authentication is a static token table, provided in the
starter — keep the name and contents exactly as given:

```python
TOKENS = {"alice-token": "alice", "bob-token": "bob"}
```

Write the token check **once** as a reusable dependency (a callable used with
`Depends(...)`) and apply it to every protected endpoint. The dependency reads
the request header `X-API-Token`:

- header missing → respond **401** with JSON `{"detail": "missing token"}`
- token not in `TOKENS` → respond **403** with JSON `{"detail": "invalid token"}`
- otherwise it resolves to the username mapped by `TOKENS`

Endpoints:

1. `GET /public` — **no auth**. Returns `{"message": "public"}` with status 200.

2. `GET /me` — protected. Returns `{"user": "<username>"}` for the caller's
   token.

3. `POST /items` — protected. JSON body validated by a pydantic model with a
   single required field `name: str`. Stores the item **for the calling user**
   in an in-memory store and returns `{"user": "<username>", "name": "<name>"}`
   with status **201**.

4. `GET /items` — protected. Returns the list of the calling user's items, in
   insertion order, each as `{"name": "<name>"}`. A user who has stored
   nothing gets `[]`. Users must never see each other's items.

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()` at
import time.

Example session:

```
GET /public                                   -> 200 {"message": "public"}
GET /me                                       -> 401 {"detail": "missing token"}
GET /me      (X-API-Token: nope)              -> 403 {"detail": "invalid token"}
GET /me      (X-API-Token: alice-token)       -> 200 {"user": "alice"}
POST /items  (X-API-Token: alice-token) {"name": "kettle"}
                                              -> 201 {"user": "alice", "name": "kettle"}
GET /items   (X-API-Token: bob-token)         -> 200 []
```
