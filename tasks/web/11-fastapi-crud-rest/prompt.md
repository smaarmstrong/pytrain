# FastAPI: a full CRUD API

In `solution.py`, build a FastAPI app (module-level `app`) managing todo
tasks in an in-memory store, with **full REST semantics**: POST, GET
(list + detail), PUT (replace), PATCH (partial update), DELETE.

Task shape (all responses): `{"id": int, "title": str, "done": bool}`.

Endpoints:

1. `POST /tasks` — body `{"title": str, "done": bool = false}` (`title`
   required, `done` optional defaulting to false; invalid bodies → 422).
   Ids start at 1 and increment; deleted ids are **never reused**.
   Returns **201** with the created task.

2. `GET /tasks` — every task in creation order. Optional query param
   `done` (bool): only tasks with that done-state.

3. `GET /tasks/{task_id}` — the task, or **404**
   `{"detail": "task not found"}`.

4. `PUT /tasks/{task_id}` — full replacement, same body schema as POST
   (`title` required — a PUT without `title` is a 422). Keeps the id.
   Returns **200** with the updated task, or **404** if absent.

5. `PATCH /tasks/{task_id}` — partial update: body may contain `title`,
   `done`, both or neither; only supplied fields change. Returns **200**
   with the updated task, or **404**.

6. `DELETE /tasks/{task_id}` — **204** with an empty body, or **404**.

Example session:

```
POST  /tasks {"title": "write docs"}       -> 201 {"id": 1, "title": "write docs", "done": false}
PUT   /tasks/1 {"title": "docs", "done": true} -> 200 {"id": 1, "title": "docs", "done": true}
PATCH /tasks/1 {"done": false}             -> 200 {"id": 1, "title": "docs", "done": false}
GET   /tasks?done=false                    -> 200 [{"id": 1, ...}]
DELETE /tasks/1                            -> 204
GET   /tasks/1                             -> 404 {"detail": "task not found"}
POST  /tasks {"title": "next"}             -> 201 {"id": 2, ...}   (id 1 not reused)
```

The grader creates its own `TestClient(app)`; do not call `uvicorn.run()`
at import time.
