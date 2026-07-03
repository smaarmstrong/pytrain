import sqlalchemy as sa
from sqlalchemy.orm import Session

from pytrain_grader import load_solution, get_attr


def fresh(mod):
    """In-memory engine + created schema for this learner module."""
    base = get_attr(mod, "Base")
    engine = sa.create_engine("sqlite+pysqlite:///:memory:")
    base.metadata.create_all(engine)
    return engine


def test_models_create_expected_tables():
    mod = load_solution()
    engine = fresh(mod)
    insp = sa.inspect(engine)
    tables = set(insp.get_table_names())
    assert {"authors", "books"} <= tables
    author_cols = {c["name"] for c in insp.get_columns("authors")}
    assert {"id", "name"} <= author_cols
    book_cols = {c["name"] for c in insp.get_columns("books")}
    assert {"id", "title", "author_id"} <= book_cols


def test_books_has_fk_to_authors():
    mod = load_solution()
    engine = fresh(mod)
    fks = sa.inspect(engine).get_foreign_keys("books")
    assert any(
        fk["referred_table"] == "authors" and "author_id" in fk["constrained_columns"]
        for fk in fks
    ), "books.author_id must be a ForeignKey to authors.id"


def test_add_author_persists_and_returns():
    mod = load_solution()
    engine = fresh(mod)
    with Session(engine) as session:
        got = get_attr(mod, "add_author")(session, "Ursula", ["Earthsea", "The Dispossessed"])
        assert got is not None
        assert got.name == "Ursula"
    # A brand-new session proves the data was committed, not just pending.
    with Session(engine) as session:
        author_cls = get_attr(mod, "Author")
        names = session.scalars(sa.select(author_cls.name)).all()
        assert names == ["Ursula"]
        book_cls = get_attr(mod, "Book")
        titles = sorted(session.scalars(sa.select(book_cls.title)).all())
        assert titles == ["Earthsea", "The Dispossessed"]


def test_relationship_author_to_books():
    mod = load_solution()
    engine = fresh(mod)
    with Session(engine) as session:
        get_attr(mod, "add_author")(session, "Iain", ["Excession", "Player of Games"])
        author_cls = get_attr(mod, "Author")
        author = session.scalars(
            sa.select(author_cls).where(author_cls.name == "Iain")
        ).one()
        assert sorted(b.title for b in author.books) == ["Excession", "Player of Games"]


def test_relationship_book_to_author():
    mod = load_solution()
    engine = fresh(mod)
    with Session(engine) as session:
        get_attr(mod, "add_author")(session, "Octavia", ["Kindred"])
        book_cls = get_attr(mod, "Book")
        book = session.scalars(
            sa.select(book_cls).where(book_cls.title == "Kindred")
        ).one()
        assert book.author.name == "Octavia"


def test_titles_by_author_sorted():
    mod = load_solution()
    engine = fresh(mod)
    with Session(engine) as session:
        get_attr(mod, "add_author")(session, "Terry", ["Mort", "Guards! Guards!", "Small Gods"])
        get_attr(mod, "add_author")(session, "Neil", ["Coraline"])
        got = get_attr(mod, "titles_by_author")(session, "Terry")
        assert got == ["Guards! Guards!", "Mort", "Small Gods"]
        assert get_attr(mod, "titles_by_author")(session, "Neil") == ["Coraline"]


def test_titles_by_author_no_books():
    mod = load_solution()
    engine = fresh(mod)
    with Session(engine) as session:
        get_attr(mod, "add_author")(session, "Silent", [])
        assert get_attr(mod, "titles_by_author")(session, "Silent") == []


def test_author_of():
    mod = load_solution()
    engine = fresh(mod)
    with Session(engine) as session:
        get_attr(mod, "add_author")(session, "Ann", ["Ancillary Justice"])
        get_attr(mod, "add_author")(session, "Becky", ["To Be Taught, If Fortunate"])
        assert get_attr(mod, "author_of")(session, "Ancillary Justice") == "Ann"
        assert get_attr(mod, "author_of")(session, "To Be Taught, If Fortunate") == "Becky"
