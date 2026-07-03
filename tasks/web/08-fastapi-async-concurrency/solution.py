import asyncio

from fastapi import FastAPI, Query

app = FastAPI()

DELAY = 0.2


async def fetch_source(name: str) -> dict:
    await asyncio.sleep(DELAY)  # pretend network I/O
    return {"source": name, "length": len(name)}


@app.get("/slow/{name}")
async def slow(name: str):
    return await fetch_source(name)


@app.get("/aggregate")
async def aggregate(sources: list[str] = Query(...)):
    results = await asyncio.gather(*(fetch_source(s) for s in sources))
    return {"results": list(results), "count": len(results)}
