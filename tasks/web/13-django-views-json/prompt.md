# Django: views, URLconf and JSON

In `solution.py`, write plain Django **function views** returning
`JsonResponse`, wired up in a module-level **`urlpatterns`** list (your
module acts as the ROOT_URLCONF — the grader points Django at it with
`override_settings(ROOT_URLCONF=...)`). No models, no templates.

Keep the settings boilerplate from the starter — it lets the file work
standalone while deferring to the grader's configuration.

## URLs and behaviour

1. `GET /ping/` → **200** `{"pong": true}`

2. `GET /square/<int:n>/` → **200** `{"result": <n*n>}`
   (use a `path()` converter — `/square/notanumber/` is a 404)

3. `GET /add/?a=<int>&b=<int>` → **200** `{"sum": <a+b>}`.
   If `a` or `b` is missing or not an integer → **400**
   `{"error": "a and b must be integers"}`

4. `POST /echo/` — parse the JSON request body and return **200**
   `{"you_sent": <the parsed body>}`.
   - a body that isn't valid JSON → **400** `{"error": "invalid json"}`
   - any other method (GET/PUT/...) → **405** (e.g. via
     `django.views.decorators.http.require_POST` or
     `HttpResponseNotAllowed`)

Examples:

```
GET  /ping/                 -> 200 {"pong": true}
GET  /square/7/             -> 200 {"result": 49}
GET  /add/?a=2&b=40         -> 200 {"sum": 42}
GET  /add/?a=2&b=fish       -> 400 {"error": "a and b must be integers"}
POST /echo/  {"x": [1, 2]}  -> 200 {"you_sent": {"x": [1, 2]}}
GET  /echo/                 -> 405
```

The grader uses `django.test.Client` — never start a server.
