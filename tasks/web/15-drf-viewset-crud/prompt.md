# DRF: serializer + ModelViewSet CRUD

In `solution.py`, build a complete Django REST Framework CRUD API for
code snippets: a model, a `ModelSerializer`, a `ModelViewSet` and router
URLs. The grader drives it with `rest_framework.test.APIClient` against
in-memory SQLite (it creates the table for you — no migrations).

Keep the settings boilerplate from the starter (note it includes
`"rest_framework"` in `INSTALLED_APPS`).

Define, at module level:

1. `Snippet` — a model with `class Meta: app_label = "solution"`:
   - `title = models.CharField(max_length=100)`
   - `code = models.TextField()`
   - `language = models.CharField(max_length=30, default="python")`

2. `SnippetSerializer` — a `ModelSerializer` over exactly the fields
   `["id", "title", "code", "language"]`.

3. `SnippetViewSet` — a `ModelViewSet` serving all snippets ordered by
   `id`.

4. `urlpatterns` — from a DRF router (e.g. `DefaultRouter`) with the
   viewset registered under the prefix **`snippets`**, so the API is:

   ```
   GET/POST       /snippets/
   GET/PUT/PATCH/DELETE  /snippets/<pk>/
   ```

Behaviour (all standard `ModelViewSet` semantics):

```
POST /snippets/ {"title": "hello", "code": "print('hi')"}
  -> 201 {"id": 1, "title": "hello", "code": "print('hi')", "language": "python"}
POST /snippets/ {"code": "no title"}     -> 400 (serializer validation)
GET  /snippets/                          -> 200 [ ...snippets by id... ]
GET  /snippets/1/                        -> 200 (the snippet)
PUT  /snippets/1/ {full body}            -> 200 (replaced)
PATCH /snippets/1/ {"language": "rust"}  -> 200 (only language changed)
DELETE /snippets/1/                      -> 204, then GET /snippets/1/ -> 404
```
