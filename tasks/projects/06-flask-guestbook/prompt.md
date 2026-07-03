# Project: Flask guestbook

Build a small guestbook web app the idiomatic Flask way: an **app factory**
in `app.py`, the routes on a **blueprint** in `entries.py`, accepting both
HTML-form and JSON submissions, responding with JSON. The grader imports
`create_app` from **`app.py`**, builds apps with it and drives them through
`app.test_client()` — no server, no ports.

## `app.py` — the factory

```python
def create_app():
    ...
```

- Returns a fresh `Flask` app on every call. Each app has its **own
  independent in-memory store** — entries added to one `create_app()` app
  must not appear in another's.
- Registers the blueprint from `entries.py` under the URL prefix
  **`/entries`**.
- Defines a health route directly in the factory: `GET /` returns JSON
  `{"status": "ok"}`.

## `entries.py` — the blueprint

Expose a module-level `Blueprint` named `bp`. An entry is
`{"id": int, "name": str, "message": str}`; ids start at 1 per app and
increment.

**`GET /entries/`** — JSON array of all entries, oldest first (`[]` when
empty), status 200.

**`POST /entries/`** — create an entry from fields `name` and `message`,
accepted **either** as form data (`request.form`) **or** as a JSON body.
Strip surrounding whitespace from both values and store the stripped
strings. On success: status **201**, body = the created entry as JSON.
If either field is missing or blank after stripping: status **400**, body
`{"error": "name and message are required"}` (nothing stored).

**`GET /entries/<id>`** — the entry as JSON, or status **404** with
`{"error": "not found"}`.

Note: routes are defined with a leading `/` on the blueprint, so the
external paths are `/entries/` and `/entries/<id>`.

## Acceptance example

```
GET  /                                     -> 200 {"status": "ok"}
POST /entries/  form: name=Ada&message=hi  -> 201 {"id": 1, "name": "Ada", "message": "hi"}
POST /entries/  json: {"name": "Grace", "message": "yo"}
                                           -> 201 {"id": 2, "name": "Grace", "message": "yo"}
POST /entries/  form: name=&message=x      -> 400 {"error": "name and message are required"}
GET  /entries/                             -> 200 [entry 1, entry 2]
GET  /entries/99                           -> 404 {"error": "not found"}
```
