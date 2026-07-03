import polars as pl
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def frame():
    return pl.DataFrame(
        {
            "item": ["anvil", "apple", "bolt", "bracket", "cog"],
            "category": ["tools", "food", "parts", "parts", "parts"],
            "qty": [2, 40, 100, 25, 0],
            "price": [99.5, 0.4, 0.1, 3.75, 12.0],
        }
    )


def test_select_cols():
    got = _f("select_cols")(frame(), ["item", "price"])
    assert isinstance(got, pl.DataFrame)
    assert got.columns == ["item", "price"]
    assert got["item"].to_list() == ["anvil", "apple", "bolt", "bracket", "cog"]
    assert got["price"].to_list() == pytest.approx([99.5, 0.4, 0.1, 3.75, 12.0])


def test_select_cols_order_respected():
    got = _f("select_cols")(frame(), ["qty", "item"])
    assert got.columns == ["qty", "item"]


def test_filter_at_least():
    got = _f("filter_at_least")(frame(), 25)
    assert isinstance(got, pl.DataFrame)
    assert got["item"].to_list() == ["apple", "bolt", "bracket"]


def test_filter_at_least_boundary_inclusive():
    got = _f("filter_at_least")(frame(), 100)
    assert got["item"].to_list() == ["bolt"]
    assert _f("filter_at_least")(frame(), 1000).height == 0


def test_add_revenue():
    got = _f("add_revenue")(frame())
    assert isinstance(got, pl.DataFrame)
    assert set(got.columns) == {"item", "category", "qty", "price", "revenue"}
    assert got["revenue"].to_list() == pytest.approx([199.0, 16.0, 10.0, 93.75, 0.0])


def test_add_revenue_does_not_mutate():
    df = frame()
    _f("add_revenue")(df)
    assert "revenue" not in df.columns


def test_category_totals():
    got = _f("category_totals")(frame())
    assert isinstance(got, pl.DataFrame)
    assert got.columns == ["category", "total_qty"]
    assert got.to_dicts() == [
        {"category": "food", "total_qty": 40},
        {"category": "parts", "total_qty": 125},
        {"category": "tools", "total_qty": 2},
    ]


def test_category_totals_single_category():
    df = pl.DataFrame(
        {
            "item": ["a", "b"],
            "category": ["z", "z"],
            "qty": [1, 2],
            "price": [1.0, 1.0],
        }
    )
    got = _f("category_totals")(df)
    assert got.to_dicts() == [{"category": "z", "total_qty": 3}]
