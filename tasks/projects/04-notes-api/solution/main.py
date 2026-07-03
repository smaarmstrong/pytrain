"""notes API: FastAPI CRUD with validation and an API-key auth dependency."""
from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

from auth import require_api_key

app = FastAPI()

auth = [Depends(require_api_key)]


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    body: str
    tags: list[str] = []


notes: dict[int, dict] = {}
_next_id = 1


def _not_found():
    raise HTTPException(status_code=404, detail="note not found")


@app.post("/notes", status_code=201, dependencies=auth)
def create_note(note: NoteIn):
    global _next_id
    stored = {"id": _next_id, **note.model_dump()}
    notes[_next_id] = stored
    _next_id += 1
    return stored


@app.get("/notes", dependencies=auth)
def list_notes(tag: str | None = None):
    result = list(notes.values())
    if tag is not None:
        result = [n for n in result if tag in n["tags"]]
    return result


@app.get("/notes/{note_id}", dependencies=auth)
def get_note(note_id: int):
    if note_id not in notes:
        _not_found()
    return notes[note_id]


@app.put("/notes/{note_id}", dependencies=auth)
def replace_note(note_id: int, note: NoteIn):
    if note_id not in notes:
        _not_found()
    notes[note_id] = {"id": note_id, **note.model_dump()}
    return notes[note_id]


@app.delete("/notes/{note_id}", status_code=204, dependencies=auth)
def delete_note(note_id: int):
    if note_id not in notes:
        _not_found()
    del notes[note_id]
    return Response(status_code=204)
