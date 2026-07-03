from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserIn(BaseModel):
    username: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


users: dict[int, dict] = {}
next_id = 1


@app.post("/users", status_code=201, response_model=UserOut)
def create_user(user: UserIn):
    global next_id
    if any(u["username"] == user.username for u in users.values()):
        raise HTTPException(status_code=409, detail="username taken")
    stored = {"id": next_id, **user.model_dump()}
    users[next_id] = stored
    next_id += 1
    return stored


@app.get("/users", response_model=list[UserOut])
def list_users():
    return list(users.values())


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user not found")
    return users[user_id]


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="user not found")
    del users[user_id]
    return None
