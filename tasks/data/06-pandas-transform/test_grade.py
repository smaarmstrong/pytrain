import pandas as pd
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def sample():
    return pd.DataFrame(
        {
            "product": ["anvil", "bolt", "cog", "dynamo", "elbow"],
            "qty": [0, 120, 45, 3, 0],
            "price": [99.5, 0.1, 2.5, 45.0, 1.25],
        }
    )


def test_in_stock_rows_and_index():
    out = _f("in_stock")(sample())
    assert isinstance(out, pd.DataFrame)
    assert list(out.columns) == ["product", "qty", "price"]
    assert list(out["product"]) == ["bolt", "cog", "dynamo"]
    assert list(out.index) == [0, 1, 2]


def test_in_stock_all_zero():
    df = pd.DataFrame({"product": ["a"], "qty": [0], "price": [1.0]})
    assert len(_f("in_stock")(df)) == 0


def test_in_stock_does_not_mutate():
    df = sample()
    _f("in_stock")(df)
    assert list(df["product"]) == ["anvil", "bolt", "cog", "dynamo", "elbow"]
    assert len(df) == 5


def test_top_n_by_price():
    out = _f("top_n_by")(sample(), "price", 2)
    assert list(out["product"]) == ["anvil", "dynamo"]
    assert list(out.index) == [0, 1]


def test_top_n_by_qty():
    out = _f("top_n_by")(sample(), "qty", 3)
    assert list(out["product"]) == ["bolt", "cog", "dynamo"]


def test_top_n_by_n_larger_than_frame():
    out = _f("top_n_by")(sample(), "qty", 99)
    assert len(out) == 5
    assert list(out["qty"]) == sorted(out["qty"], reverse=True)


def test_top_n_by_does_not_mutate():
    df = sample()
    _f("top_n_by")(df, "price", 2)
    assert list(df["product"]) == ["anvil", "bolt", "cog", "dynamo", "elbow"]


def test_with_total_values():
    out = _f("with_total")(sample())
    assert list(out.columns) == ["product", "qty", "price", "total"]
    assert list(out["total"]) == pytest.approx([0.0, 12.0, 112.5, 135.0, 0.0])
    assert out["total"].dtype.kind == "f"


def test_with_total_keeps_original_data():
    out = _f("with_total")(sample())
    assert list(out["product"]) == ["anvil", "bolt", "cog", "dynamo", "elbow"]
    assert list(out["qty"]) == [0, 120, 45, 3, 0]


def test_with_total_does_not_mutate():
    df = sample()
    _f("with_total")(df)
    assert "total" not in df.columns
