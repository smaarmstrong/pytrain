from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# class Author(Base): ...
# class Book(Base): ...


def add_author(session, name, titles):
    """Create Author + Books, commit, return the Author."""
    raise NotImplementedError


def titles_by_author(session, name):
    """Sorted list of the author's book titles."""
    raise NotImplementedError


def author_of(session, title):
    """Name of the author who wrote `title`."""
    raise NotImplementedError
