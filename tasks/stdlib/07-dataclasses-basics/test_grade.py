import pytest

from pytrain_grader import load_solution, get_attr


def test_book_positional_and_keyword_construction():
    Book = get_attr(load_solution(), "Book")
    b = Book("Dune", "Herbert")
    assert (b.title, b.author) == ("Dune", "Herbert")
    b2 = Book(title="Dune", author="Herbert", pages=412, tags=["scifi"])
    assert (b2.pages, b2.tags) == (412, ["scifi"])


def test_book_defaults():
    Book = get_attr(load_solution(), "Book")
    b = Book("Dune", "Herbert")
    assert b.pages == 0
    assert b.tags == []


def test_book_equality_by_value():
    Book = get_attr(load_solution(), "Book")
    assert Book("Dune", "Herbert") == Book("Dune", "Herbert")
    assert Book("Dune", "Herbert") != Book("Dune", "Herbert", pages=1)
    assert Book("Dune", "Herbert") != Book("Emma", "Austen")


def test_book_tags_default_not_shared():
    Book = get_attr(load_solution(), "Book")
    a, b = Book("A", "x"), Book("B", "y")
    a.tags.append("classic")
    assert a.tags == ["classic"]
    assert b.tags == []


def test_point_is_frozen():
    Point = get_attr(load_solution(), "Point")
    p = Point(1, 2)
    with pytest.raises(AttributeError):
        p.x = 99


def test_point_equality_and_hash():
    Point = get_attr(load_solution(), "Point")
    assert Point(1, 2) == Point(1, 2)
    assert Point(1, 2) != Point(2, 1)
    assert len({Point(1, 2), Point(1, 2), Point(3, 4)}) == 2
    d = {Point(1, 2): "here"}
    assert d[Point(1, 2)] == "here"


def test_point_ordering_field_by_field():
    Point = get_attr(load_solution(), "Point")
    assert Point(1, 2) < Point(1, 9)
    assert Point(1, 9) < Point(2, 1)
    assert Point(2, 1) > Point(1, 9)
    assert Point(1, 2) <= Point(1, 2)
    pts = [Point(2, 1), Point(1, 9), Point(1, 2)]
    assert sorted(pts) == [Point(1, 2), Point(1, 9), Point(2, 1)]
