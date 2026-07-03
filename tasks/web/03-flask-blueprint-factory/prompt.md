# Flask: blueprint + app factory

In `solution.py`, structure a Flask app the scalable way: routes live on a
**blueprint**, and apps are built by an **application factory** — no
module-level `app` this time.

Define:

1. `api_bp` — a module-level `flask.Blueprint` holding all the routes
   below.

2. `create_app(config=None)` — a factory that:
   - creates a fresh `Flask` app,
   - if `config` (a dict) is given, applies it with `app.config.update(config)`,
   - registers `api_bp` under the URL prefix **`/api/v1`**,
   - returns the app.

   Every call must return a **new, independent** app: config and request
   counters must not leak between instances.

## Routes (all under `/api/v1` via the blueprint)

- `GET /api/v1/status` — returns
  `{"status": "ok", "app_name": <app.config["APP_NAME"] or "default">}`.
  `"default"` is used when the factory was called without an `APP_NAME`.

- `GET /api/v1/double/<int:n>` — returns `{"result": <2*n>}`.

- `POST /api/v1/hits` — a per-application counter starting at 0: each call
  increments it and returns `{"hits": <new count>}` with status 200. Two
  apps created by two `create_app()` calls count independently (store the
  counter on the app — e.g. in `app.config` or `app.extensions` — not in a
  module-level global).

Example:

```python
one = create_app({"APP_NAME": "one"})
two = create_app()
one.test_client().get("/api/v1/status").get_json()
#  -> {"status": "ok", "app_name": "one"}
two.test_client().get("/api/v1/status").get_json()
#  -> {"status": "ok", "app_name": "default"}
one.test_client().post("/api/v1/hits").get_json()   # {"hits": 1}
two.test_client().post("/api/v1/hits").get_json()   # {"hits": 1}  (own counter)
```

The grader calls `create_app(...)` itself and uses `test_client()`; do not
create a module-level app or call `app.run()`.
