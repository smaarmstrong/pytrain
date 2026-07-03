import pandas as pd
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def grader_df():
    return pd.DataFrame(
        {
            "sku": ["X1", "X2", "Y1"],
            "name": ["widget", "washer", "yoke"],
            "qty": [7, 0, 12],
            "price": [1.5, 0.05, 20.0],
        }
    )


def test_make_inventory_columns_and_index():
    df = _f("make_inventory")()
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["sku", "name", "qty", "price"]
    assert list(df.index) == [0, 1, 2, 3]


def test_make_inventory_values():
    df = _f("make_inventory")()
    assert list(df["sku"]) == ["A1", "A2", "B1", "B2"]
    assert list(df["name"]) == ["anvil", "apple", "bolt", "bracket"]
    assert list(df["qty"]) == [10, 40, 300, 25]
    assert list(df["price"]) == pytest.approx([99.5, 0.4, 0.1, 3.75])


def test_make_inventory_dtypes():
    df = _f("make_inventory")()
    assert df["qty"].dtype.kind in ("i", "u"), "qty must be an integer dtype"
    assert df["price"].dtype.kind == "f", "price must be a float dtype"


def test_first_n_names():
    got = _f("first_n_names")(grader_df(), 2)
    assert isinstance(got, list)
    assert got == ["widget", "washer"]


def test_first_n_names_all_rows():
    assert _f("first_n_names")(grader_df(), 3) == ["widget", "washer", "yoke"]


def test_first_n_names_zero():
    assert _f("first_n_names")(grader_df(), 0) == []


def test_row_by_sku():
    got = _f("row_by_sku")(grader_df(), "X2")
    assert isinstance(got, dict)
    assert set(got) == {"sku", "name", "qty", "price"}
    assert got["sku"] == "X2"
    assert got["name"] == "washer"
    assert got["qty"] == 0
    assert got["price"] == pytest.approx(0.05)


def test_row_by_sku_last_row():
    got = _f("row_by_sku")(grader_df(), "Y1")
    assert got["name"] == "yoke"
    assert got["qty"] == 12


def test_numeric_summary():
    got = _f("numeric_summary")(grader_df())
    assert set(got) == {"total_qty", "max_price"}
    assert got["total_qty"] == 19
    assert got["max_price"] == pytest.approx(20.0)
