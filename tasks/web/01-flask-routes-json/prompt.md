# Flask: routes, params and JSON

In `solution.py`, build a Flask application exposed as a module-level
variable named `app`, with a tiny in-memory notes store:

```python
from flask import Flask
app = Flask(__name__)
```

Endpoints:

1. `GET /ping` — returns JSON `{"pong": true}` with status **200**.

2. `GET /greet/<name>` — URL param plus an optional query string
   `greeting` (default `"Hello"`). Returns
   `{"message": "<greeting>, <name>!"}`.

   ```
   GET /greet/Ada              -> 200 {"message": "Hello, Ada!"}
   GET /greet/Ada?greeting=Hi  -> 200 {"message": "Hi, Ada!"}
   ```

3. `POST /notes` — accepts a JSON body `{"text": "<string>"}`. Stores the
   note with an integer `id` starting at 1 and incrementing. Returns the
   stored note `{"id": 1, "text": "..."}` with status **201**.

4. `GET /notes` — returns the JSON list of all notes (each
   `{"id": ..., "text": ...}`), in insertion order. Optional query param
   `contains` — only notes whose text contains that substring
   (case-sensitive).

5. `GET /notes/<int:note_id>` — returns the note with that id, or status
   **404** with JSON `{"error": "not found"}` if absent.

The grader uses `app.test_client()`; do not call `app.run()` at import
time.
