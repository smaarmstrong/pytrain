# FastAPI: shaped responses and status codes

In `solution.py`, build a FastAPI app (module-level `app`) managing users.
Internally each user record stores a `password` — which must **never**
appear in any response. Shape what goes out with `response_model` (or an
equivalent output model), signal errors with `HTTPException`, and use
precise status codes.

Input model: `username: str`, `email: str`, `password: str` (all
required — invalid bodies get FastAPI's usual 422).

Public user shape (what responses contain): `{"id": int, "username": str,
"email": str}` — exactly these keys, no `password`.

Endpoints:

1. `POST /users` — create a user, ids from 1 incrementing. Status
   **201**, returns the public shape. If the username is already taken:
   **409** with `{"detail": "username taken"}`.

2. `GET /users` — list of all users in creation order, public shape only.

3. `GET /users/{user_id}` — public shape, or **404** with
   `{"detail": "user not found"}`.

4. `DELETE /users/{user_id}` — **204** with an **empty body** on success
   (hint: `status_code=204` and return `None`), or **404** with
   `{"detail": "user not found"}`. Deleting twice → second call is 404.
   A deleted username can be registered again (no 409).

Example session:

```
POST /users {"username": "ada", "email": "ada@example.com", "password": "s3cret"}
  -> 201 {"id": 1, "username": "ada", "email": "ada@example.com"}
POST /users {same username}   -> 409 {"detail": "username taken"}
GET  /users/1                 -> 200 {"id": 1, "username": "ada", "email": "ada@example.com"}
DELETE /users/1               -> 204 (empty body)
DELETE /users/1               -> 404 {"detail": "user not found"}
```

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()`
at import time.
