from fastapi import FastAPI

TOKENS = {"alice-token": "alice", "bob-token": "bob"}

app = FastAPI()

# Write one token-check dependency and reuse it on /me and /items.
# Endpoints: GET /public, GET /me, POST /items, GET /items — see prompt.md
