# FastAPI: path, query and body

In `solution.py`, build a FastAPI application exposed as a module-level
variable named `app`, with an in-memory book catalogue:

```python
from fastapi import FastAPI
app = FastAPI()
```

Endpoints:

1. `POST /books` — accepts a JSON body validated by a pydantic model with
   fields `title: str`, `author: str`, `year: int` (all required). Assigns the
   book an integer `id` starting at 1 and incrementing. Returns the stored
   book **including its id** with status **201**. A body missing a required
   field or with a non-integer `year` must be rejected by validation (FastAPI
   returns 422 for you if you use a pydantic model).

2. `GET /books/{book_id}` — path param, returns the book with that id, or
   status **404** with JSON `{"detail": "book not found"}` if absent.

3. `GET /books` — returns a list of all books. Optional query params:
   - `author: str` — only books whose author matches exactly
   - `limit: int` (default 10) — at most this many results

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()` at
import time.

Example session:

```
POST /books {"title": "Fluent Python", "author": "Ramalho", "year": 2022}
  -> 201 {"id": 1, "title": "Fluent Python", "author": "Ramalho", "year": 2022}
GET /books/1          -> 200 (the book)
GET /books/99         -> 404 {"detail": "book not found"}
GET /books?author=Ramalho&limit=5 -> 200 [ ...only Ramalho's books... ]
```
