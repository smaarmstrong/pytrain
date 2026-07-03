from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    books: Mapped[list["Book"]] = relationship(back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship(back_populates="books")


def add_author(session, name, titles):
    author = Author(name=name, books=[Book(title=t) for t in titles])
    session.add(author)
    session.commit()
    return author


def titles_by_author(session, name):
    author = session.scalars(select(Author).where(Author.name == name)).one()
    return sorted(book.title for book in author.books)


def author_of(session, title):
    book = session.scalars(select(Book).where(Book.title == title)).one()
    return book.author.name
