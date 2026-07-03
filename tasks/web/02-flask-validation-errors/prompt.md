# Flask: validate and abort

In `solution.py`, build a Flask app (module-level `app`) that validates
incoming data and returns **JSON error bodies for every error**, using
`abort()` plus custom error handlers.

## Error handlers (app-wide)

- **404** — every 404, including completely unknown URLs, must return JSON
  `{"error": "not found", "path": "<request path>"}` with status 404.

  ```
  GET /no/such/page -> 404 {"error": "not found", "path": "/no/such/page"}
  ```

- **400** — every 400 must return JSON
  `{"error": "bad request", "detail": "<message>"}` with status 400. The
  message is whatever description the aborting code supplied — use
  `abort(400, description="...")` and read it from the exception's
  `.description` in the handler.

## Routes

1. `POST /items` — expects a JSON object with:
   - `name` — a non-empty string. Missing, empty, or not a string (or the
     body missing / not a JSON object) → **400** with detail
     `"name is required"`.
   - `price` — an int or float `>= 0`. Missing, not a number, or negative
     → **400** with detail `"price must be a non-negative number"`.

   Check `name` first (if both are invalid, the `name` message wins).
   On success: store the item, return `{"id": <int from 1>, "name": ...,
   "price": ...}` with status **201**.

2. `GET /items/<int:item_id>` — the stored item as
   `{"id": ..., "name": ..., "price": ...}`, or a 404 (through the same
   JSON 404 handler) when absent.

The grader uses `app.test_client()`; do not call `app.run()` at import
time.
