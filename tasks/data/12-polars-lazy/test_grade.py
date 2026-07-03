import polars as pl
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def lazy_frame():
    return pl.DataFrame(
        {
            "category": ["a", "a", "b", "b", "c", "d"],
            "qty": [2, 3, 5, 1, 0, 4],
            "price": [1.0, 2.0, 3.0, 4.0, 100.0, 0.25],
        }
    ).lazy()
    # revenues (qty>0 only): a=2*1+3*2=8, b=5*3+1*4=19, d=1.0; c filtered out


def test_query_stays_lazy():
    got = _f("top_categories_query")(lazy_frame(), 2)
    assert isinstance(got, pl.LazyFrame), (
        "top_categories_query must return a LazyFrame — do not .collect() inside it"
    )
    assert not isinstance(got, pl.DataFrame)


def test_query_collects_to_expected_rows():
    q = _f("top_categories_query")(lazy_frame(), 2)
    out = q.collect()
    assert out.columns == ["category", "revenue"]
    assert out["category"].to_list() == ["b", "a"]
    assert out["revenue"].to_list() == pytest.approx([19.0, 8.0])


def test_collected_result():
    got = _f("top_categories")(lazy_frame(), 2)
    assert isinstance(got, pl.DataFrame)
    assert got["category"].to_list() == ["b", "a"]
    assert got["revenue"].to_list() == pytest.approx([19.0, 8.0])


def test_zero_qty_rows_filtered_out():
    got = _f("top_categories")(lazy_frame(), 10)
    cats = got["category"].to_list()
    assert "c" not in cats, "rows with qty <= 0 must be filtered before aggregating"
    assert cats == ["b", "a", "d"]
    assert got["revenue"].to_list() == pytest.approx([19.0, 8.0, 1.0])


def test_head_limits_rows():
    assert _f("top_categories")(lazy_frame(), 1).height == 1
    assert _f("top_categories")(lazy_frame(), 3).height == 3


def test_n_larger_than_categories():
    got = _f("top_categories")(lazy_frame(), 99)
    assert got.height == 3
