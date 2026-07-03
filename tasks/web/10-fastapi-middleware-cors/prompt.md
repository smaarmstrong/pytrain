# FastAPI: middleware, CORS and headers

In `solution.py`, build a FastAPI app (module-level `app`) whose
cross-cutting behaviour lives in **middleware**, not in the endpoints.

## Endpoints (trivial on purpose)

- `GET /ping` — returns `{"pong": true}`.
- `GET /teapot` — returns status **418** with `{"detail": "I'm a teapot"}`.

## 1. Custom header middleware

Add an HTTP middleware (`@app.middleware("http")` or a raw ASGI/
`BaseHTTPMiddleware` class) that stamps **every** response — including
404s for unknown paths and error responses — with:

- `X-API-Version: 1.0`
- `X-Request-Id` — echo the request's `X-Request-Id` header if the client
  sent one; otherwise generate a non-empty id (e.g. `uuid4().hex`).

## 2. CORS

Add `CORSMiddleware` configured to:

- allow **only** the origin `https://app.example.com`
- allow methods `GET` and `POST`
- allow the request header `X-Request-Id`

Behaviour the grader checks (this is what the middleware does for you
when configured correctly):

```
# simple request from the allowed origin
GET /ping  (Origin: https://app.example.com)
  -> access-control-allow-origin: https://app.example.com

# preflight
OPTIONS /ping  (Origin: https://app.example.com,
                Access-Control-Request-Method: GET)
  -> 200, access-control-allow-origin: https://app.example.com

# preflight from anywhere else must NOT be granted
OPTIONS /ping  (Origin: https://evil.example.com, ...)
  -> no access-control-allow-origin for that origin (and not "*")
```

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()`
at import time.
