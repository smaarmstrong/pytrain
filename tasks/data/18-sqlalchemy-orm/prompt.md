# SQLAlchemy ORM: models & relationships

In `solution.py`, using the SQLAlchemy 2.x ORM, define two mapped classes
and three query helpers.

Models (module level):

```python
class Base(...):        # your declarative base (subclass DeclarativeBase)
    ...

class Author(Base):
    """Table 'authors': id (int, primary key), name (str).
    `author.books` is the list of the author's Book objects."""

class Book(Base):
    """Table 'books': id (int, primary key), title (str),
    author_id (foreign key -> authors.id).
    `book.author` is the owning Author object (the inverse of Author.books)."""
```

Helpers (each takes an active `sqlalchemy.orm.Session`):

```python
def add_author(session, name, titles):
    """Create an Author plus one Book per title, persist and commit them.
    Return the Author object."""

def titles_by_author(session, name):
    """The titles of that author's books, sorted alphabetically, as
    list[str]. The author exists and is unique."""

def author_of(session, title):
    """The NAME (str) of the author of the book with this title.
    The title exists and is unique."""
```

The grader creates an in-memory SQLite engine itself, runs
`Base.metadata.create_all(engine)`, and exercises the relationship in both
directions — so wire up `relationship(...)` properly on both classes.

Example:

```python
>>> a = add_author(session, "Ursula", ["Earthsea", "The Dispossessed"])
>>> titles_by_author(session, "Ursula")
['Earthsea', 'The Dispossessed']
>>> author_of(session, "Earthsea")
'Ursula'
```
