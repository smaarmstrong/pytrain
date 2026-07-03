import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()


@app.middleware("http")
async def stamp_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-API-Version"] = "1.0"
    response.headers["X-Request-Id"] = request.headers.get(
        "X-Request-Id", uuid.uuid4().hex
    )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["X-Request-Id"],
)


@app.get("/ping")
def ping():
    return {"pong": True}


@app.get("/teapot")
def teapot():
    return JSONResponse(status_code=418, content={"detail": "I'm a teapot"})
