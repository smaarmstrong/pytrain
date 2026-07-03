import asyncio

from fastapi import FastAPI

app = FastAPI()

DELAY = 0.2


async def fetch_source(name: str) -> dict:
    await asyncio.sleep(DELAY)  # pretend network I/O
    return {"source": name, "length": len(name)}


# GET /slow/{name}, GET /aggregate?sources=... — see prompt.md.
# Both endpoints must be async def and must not block the event loop.
