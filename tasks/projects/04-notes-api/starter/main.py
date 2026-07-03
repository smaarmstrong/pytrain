"""notes API — the grader does `from main import app` and wraps it in
fastapi.testclient.TestClient.

Define the pydantic model, the CRUD routes and wire in the auth dependency
from auth.py. See prompt.md for the exact route table, status codes and
error bodies.
"""

# from fastapi import FastAPI, Depends, HTTPException
# from auth import require_api_key

# app = FastAPI()
