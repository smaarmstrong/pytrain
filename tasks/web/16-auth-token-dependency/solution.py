from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

TOKENS = {"alice-token": "alice", "bob-token": "bob"}

app = FastAPI()

items: dict[str, list[dict]] = {}


def require_user(x_api_token: str | None = Header(default=None)) -> str:
    if x_api_token is None:
        raise HTTPException(status_code=401, detail="missing token")
    user = TOKENS.get(x_api_token)
    if user is None:
        raise HTTPException(status_code=403, detail="invalid token")
    return user


class ItemIn(BaseModel):
    name: str


@app.get("/public")
def public():
    return {"message": "public"}


@app.get("/me")
def me(user: str = Depends(require_user)):
    return {"user": user}


@app.post("/items", status_code=201)
def add_item(item: ItemIn, user: str = Depends(require_user)):
    items.setdefault(user, []).append({"name": item.name})
    return {"user": user, "name": item.name}


@app.get("/items")
def list_items(user: str = Depends(require_user)):
    return items.get(user, [])
