from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TaskIn(BaseModel):
    title: str
    done: bool = False


class TaskPatch(BaseModel):
    title: str | None = None
    done: bool | None = None


tasks: dict[int, dict] = {}
next_id = 1


def _get_or_404(task_id: int) -> dict:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="task not found")
    return tasks[task_id]


@app.post("/tasks", status_code=201)
def create_task(body: TaskIn):
    global next_id
    task = {"id": next_id, "title": body.title, "done": body.done}
    tasks[next_id] = task
    next_id += 1
    return task


@app.get("/tasks")
def list_tasks(done: bool | None = None):
    out = list(tasks.values())
    if done is not None:
        out = [t for t in out if t["done"] is done]
    return out


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return _get_or_404(task_id)


@app.put("/tasks/{task_id}")
def replace_task(task_id: int, body: TaskIn):
    _get_or_404(task_id)
    task = {"id": task_id, "title": body.title, "done": body.done}
    tasks[task_id] = task
    return task


@app.patch("/tasks/{task_id}")
def patch_task(task_id: int, body: TaskPatch):
    task = _get_or_404(task_id)
    updates = body.model_dump(exclude_unset=True)
    task.update(updates)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    _get_or_404(task_id)
    del tasks[task_id]
    return None
