from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class BookIn(BaseModel):
    title: str
    author: str
    year: int


books: dict[int, dict] = {}
next_id = 1


@app.post("/books", status_code=201)
def create_book(book: BookIn):
    global next_id
    stored = {"id": next_id, **book.model_dump()}
    books[next_id] = stored
    next_id += 1
    return stored


@app.get("/books/{book_id}")
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="book not found")
    return books[book_id]


@app.get("/books")
def list_books(author: str | None = None, limit: int = 10):
    out = list(books.values())
    if author is not None:
        out = [b for b in out if b["author"] == author]
    return out[:limit]
