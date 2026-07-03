import pandas as pd
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def sales():
    return pd.DataFrame({"product_id": [1, 2, 4], "units": [5, 3, 2]})


def products():
    return pd.DataFrame({"product_id": [1, 2, 3], "name": ["anvil", "bolt", "clamp"]})


def _rows(df, cols):
    """Order-insensitive comparison helper: sorted list of value tuples."""
    return sorted(df[cols].itertuples(index=False, name=None))


def test_inner_keeps_only_matches():
    got = _f("merge_sales")(sales(), products(), "inner")
    assert isinstance(got, pd.DataFrame)
    assert set(got.columns) >= {"product_id", "units", "name"}
    assert _rows(got, ["product_id", "units", "name"]) == [
        (1, 5, "anvil"),
        (2, 3, "bolt"),
    ]


def test_left_keeps_all_sales_with_nan():
    got = _f("merge_sales")(sales(), products(), "left")
    assert len(got) == 3
    assert sorted(got["product_id"].tolist()) == [1, 2, 4]
    unmatched = got.loc[got["product_id"] == 4]
    assert len(unmatched) == 1
    assert unmatched["name"].isna().all()


def test_outer_keeps_both_sides():
    got = _f("merge_sales")(sales(), products(), "outer")
    assert len(got) == 4
    assert sorted(got["product_id"].tolist()) == [1, 2, 3, 4]
    only_product = got.loc[got["product_id"] == 3]
    assert only_product["units"].isna().all()
    only_sale = got.loc[got["product_id"] == 4]
    assert only_sale["name"].isna().all()


def test_merge_does_not_mutate_inputs():
    s, p = sales(), products()
    _f("merge_sales")(s, p, "outer")
    assert list(s.columns) == ["product_id", "units"] and len(s) == 3
    assert list(p.columns) == ["product_id", "name"] and len(p) == 3


def test_orders_with_names_order_and_nan():
    orders = pd.DataFrame({"order_id": [10, 11, 12], "customer_id": [2, 1, 9]})
    customers = pd.DataFrame({"customer_id": [1, 2, 3], "name": ["Ann", "Bob", "Cy"]})
    got = _f("orders_with_names")(orders, customers)
    assert len(got) == 3
    assert got["order_id"].tolist() == [10, 11, 12], "orders must keep their original order"
    assert got["name"].tolist()[:2] == ["Bob", "Ann"]
    assert got["name"].isna().tolist() == [False, False, True]


def test_stack_frames():
    a = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    b = pd.DataFrame({"x": [3], "y": ["c"]})
    c = pd.DataFrame({"x": [4, 5], "y": ["d", "e"]})
    got = _f("stack_frames")([a, b, c])
    assert isinstance(got, pd.DataFrame)
    assert list(got.index) == [0, 1, 2, 3, 4], "index must be a fresh RangeIndex"
    assert got["x"].tolist() == [1, 2, 3, 4, 5]
    assert got["y"].tolist() == ["a", "b", "c", "d", "e"]


def test_stack_frames_single():
    a = pd.DataFrame({"x": [7], "y": ["z"]})
    got = _f("stack_frames")([a])
    assert got["x"].tolist() == [7]
    assert list(got.index) == [0]
