import pytest

from pytrain_grader import load_solution, get_attr


TITLES = ["Dune", "Emma", "Hamlet", "Iliad"]


def shelf_cls():
    return get_attr(load_solution(), "Shelf")


def test_len():
    Shelf = shelf_cls()
    assert len(Shelf(TITLES)) == 4
    assert len(Shelf([])) == 0


def test_indexing_incl_negative():
    Shelf = shelf_cls()
    s = Shelf(TITLES)
    assert s[0] == "Dune"
    assert s[2] == "Hamlet"
    assert s[-1] == "Iliad"
    assert s[-4] == "Dune"


def test_out_of_range_raises_indexerror():
    Shelf = shelf_cls()
    s = Shelf(TITLES)
    with pytest.raises(IndexError):
        s[4]
    with pytest.raises(IndexError):
        s[-5]
    with pytest.raises(IndexError):
        Shelf([])[0]


def test_slicing_returns_shelf():
    Shelf = shelf_cls()
    s = Shelf(TITLES)
    sub = s[1:3]
    assert isinstance(sub, Shelf)
    assert list(sub) == ["Emma", "Hamlet"]
    assert list(s[::2]) == ["Dune", "Hamlet"]
    assert list(s[::-1]) == list(reversed(TITLES))
    assert list(s[10:]) == []


def test_membership():
    Shelf = shelf_cls()
    s = Shelf(TITLES)
    assert "Emma" in s
    assert "emma" not in s
    assert "Odyssey" not in s
    assert "Dune" not in Shelf([])


def test_iteration_order_and_reiterability():
    Shelf = shelf_cls()
    s = Shelf(TITLES)
    assert list(s) == TITLES
    assert list(s) == TITLES  # second full pass
    it1, it2 = iter(s), iter(s)
    assert next(it1) == "Dune"
    assert next(it2) == "Dune"  # independent iterators
    assert next(it1) == "Emma"


def test_stores_a_copy():
    Shelf = shelf_cls()
    src = ["A", "B"]
    s = Shelf(src)
    src.append("C")
    assert len(s) == 2 and list(s) == ["A", "B"]


def test_accepts_any_iterable_and_bool():
    Shelf = shelf_cls()
    s = Shelf(t for t in ("X", "Y"))
    assert list(s) == ["X", "Y"]
    assert bool(s) is True
    assert bool(Shelf([])) is False
