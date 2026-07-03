# Flask: session login

In `solution.py`, build a Flask app (module-level `app`) that keeps
per-browser state in the **signed session cookie**. Set a
`secret_key` on the app or sessions won't work.

Credentials: any username is accepted as long as the password is exactly
`"open-sesame"`.

Endpoints:

1. `POST /login` — JSON body `{"username": "<str>", "password": "<str>"}`.
   - Correct password: store the username in `session`, return **200**
     `{"user": "<username>"}`.
   - Anything else (wrong/missing password or missing username): **401**
     `{"error": "invalid credentials"}`, and the session must NOT be
     logged in afterwards.

2. `GET /whoami` —
   - logged in: **200** `{"user": "<username>"}`
   - not logged in: **401** `{"error": "not logged in"}`

3. `POST /logout` — clears the login (idempotent; fine to call when not
   logged in). Returns **200** `{"user": null}`. A following `/whoami`
   is 401 again.

4. `GET /visits` — a per-session page counter, independent of login:
   first visit from a fresh client returns `{"visits": 1}`, then
   `{"visits": 2}`, and so on. Two different clients (different cookie
   jars) each get their own count.

All state must live in the session cookie — two `test_client()` instances
of the same app must be fully independent (the grader checks this).

The grader uses `app.test_client()` (which persists cookies across
requests, like a browser); do not call `app.run()` at import time.
