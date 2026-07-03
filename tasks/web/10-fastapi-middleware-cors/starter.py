from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. custom middleware: X-API-Version + X-Request-Id on every response
# 2. CORSMiddleware: only https://app.example.com, GET/POST, X-Request-Id
# endpoints: GET /ping, GET /teapot — see prompt.md
