# Project: notes REST API

Build a complete CRUD API for notes with FastAPI: pydantic validation, an
API-key auth dependency, and an in-memory store. The grader imports `app`
from **`main.py`** and drives it through `fastapi.testclient.TestClient`
(an httpx client) — do not call `uvicorn.run()` at import time.
`auth.py` is scaffolded for the auth layer; only `main.py`'s `app` is graded.

## Auth

Every `/notes` route requires the request header `X-API-Key` to equal
exactly **`sekrit-123`**. Implement this as a **dependency** (`Depends`)
shared by all routes — a missing or wrong key must get status **401** with
body `{"detail": "invalid API key"}` from every endpoint below.

## Data model

A note is `{"id": int, "title": str, "body": str, "tags": [str, ...]}`.
Requests are validated by a pydantic model:

- `title: str` — required, 1–100 characters (use `Field(min_length=1,
  max_length=100)`)
- `body: str` — required
- `tags: list[str]` — optional, defaults to `[]`

Invalid bodies (missing field, empty or over-long title, `tags` not a list)
must be rejected with **422** — pydantic does this for you.

## Endpoints

| method & path        | behaviour |
|----------------------|-----------|
| `POST /notes`        | create; ids are integers starting at 1, incrementing; returns the stored note incl. `id`, status **201** |
| `GET /notes`         | list all notes (creation order). Optional query param `tag`: only notes whose `tags` contain it |
| `GET /notes/{id}`    | the note, or **404** `{"detail": "note not found"}` |
| `PUT /notes/{id}`    | full replace (same validated model); returns the updated note; **404** if absent, **422** if invalid |
| `DELETE /notes/{id}` | **204** with empty body; **404** if absent |

Store notes in a module-level dict/list — no database.

## Acceptance example

```
POST /notes  (X-API-Key: sekrit-123)  {"title": "shopping", "body": "milk", "tags": ["home"]}
  -> 201 {"id": 1, "title": "shopping", "body": "milk", "tags": ["home"]}
GET /notes/1  (no key)          -> 401 {"detail": "invalid API key"}
GET /notes?tag=home             -> 200 [ ...only notes tagged home... ]
PUT /notes/1  {"title": "x", "body": "y"}  -> 200 {"id": 1, "title": "x", "body": "y", "tags": []}
DELETE /notes/1                 -> 204 (empty body)
GET /notes/1                    -> 404 {"detail": "note not found"}
```
