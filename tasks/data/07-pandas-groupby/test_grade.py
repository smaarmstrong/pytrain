import pandas as pd
import pandas.testing as pdt
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def sales():
    return pd.DataFrame(
        {
            "region": ["north", "north", "south", "south", "south", "east"],
            "product": ["a", "b", "a", "b", "c", "a"],
            "units": [10, 5, 8, 12, 1, 7],
            "revenue": [100.0, 50.0, 90.0, 140.0, 5.0, 70.0],
        }
    )


def test_region_summary_shape():
    out = _f("region_summary")(sales())
    assert isinstance(out, pd.DataFrame)
    assert list(out.columns) == ["region", "total_units", "total_revenue", "avg_units"]
    assert list(out.index) == [0, 1, 2]


def test_region_summary_values():
    out = _f("region_summary")(sales())
    expected = pd.DataFrame(
        {
            "region": ["east", "north", "south"],
            "total_units": [7, 15, 21],
            "total_revenue": [70.0, 150.0, 235.0],
            "avg_units": [7.0, 7.5, 7.0],
        }
    )
    pdt.assert_frame_equal(out, expected, check_dtype=False, check_exact=False)


def test_region_summary_single_region():
    df = pd.DataFrame(
        {"region": ["west", "west"], "product": ["a", "b"],
         "units": [2, 4], "revenue": [1.0, 3.0]}
    )
    out = _f("region_summary")(df)
    assert len(out) == 1
    assert out.loc[0, "region"] == "west"
    assert out.loc[0, "total_units"] == 6
    assert out.loc[0, "avg_units"] == pytest.approx(3.0)


def test_top_region():
    assert _f("top_region")(sales()) == "south"


def test_top_region_other_data():
    df = sales()
    df.loc[5, "revenue"] = 1000.0  # east becomes the top earner
    assert _f("top_region")(df) == "east"


def test_product_units():
    got = _f("product_units")(sales())
    assert dict(got) == {"a": 25, "b": 17, "c": 1}


def test_product_units_single_product():
    df = pd.DataFrame(
        {"region": ["north"], "product": ["z"], "units": [3], "revenue": [1.0]}
    )
    assert dict(_f("product_units")(df)) == {"z": 3}
