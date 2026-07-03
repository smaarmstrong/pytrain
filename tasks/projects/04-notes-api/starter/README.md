# notes REST API — scaffold

`main.py` must expose the FastAPI application as a module-level variable
named `app` — that is what the grader imports and drives with
`TestClient(app)`. `auth.py` is a suggested home for the API-key dependency;
how you split the code is up to you.

Try it interactively with `uvicorn main:app --reload` if you like, but never
call `uvicorn.run()` at import time.
