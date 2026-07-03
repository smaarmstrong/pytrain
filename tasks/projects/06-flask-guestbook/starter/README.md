# Flask guestbook — scaffold

`app.py` holds the app factory `create_app()` (what the grader imports);
`entries.py` holds the blueprint `bp` with the guestbook routes.

The grader builds apps with `create_app()` and uses `app.test_client()` —
each factory call must produce an app with its own independent entry store.
