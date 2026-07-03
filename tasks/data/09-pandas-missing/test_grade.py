import pandas as pd
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def messy():
    return pd.DataFrame(
        {
            "name": ["ann", None, "cyd", "dee"],
            "qty": [1.0, None, 3.0, None],
            "grade": ["x", "y", None, "z"],
        }
    )


def test_missing_counts():
    got = _f("missing_counts")(messy())
    assert got == {"name": 1, "qty": 2, "grade": 1}
    assert all(type(v) is int for v in got.values()), "counts must be plain Python ints"


def test_missing_counts_none_missing():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
    assert _f("missing_counts")(df) == {"a": 0, "b": 0}


def test_fill_defaults():
    got = _f("fill_defaults")(messy(), {"qty": 0.0, "grade": "?"})
    assert got["qty"].tolist() == pytest.approx([1.0, 0.0, 3.0, 0.0])
    assert got["grade"].tolist() == ["x", "y", "?", "z"]
    assert got["name"].isna().sum() == 1, "columns not in defaults keep their NaNs"


def test_fill_defaults_does_not_mutate():
    df = messy()
    _f("fill_defaults")(df, {"qty": 0.0})
    assert df["qty"].isna().sum() == 2, "the input DataFrame must not be modified"


def test_drop_incomplete_single_column():
    got = _f("drop_incomplete")(messy(), ["qty"])
    assert len(got) == 2
    assert got["name"].tolist() == ["ann", "cyd"]


def test_drop_incomplete_multiple_columns():
    got = _f("drop_incomplete")(messy(), ["qty", "grade"])
    assert got["name"].tolist() == ["ann"]


def test_drop_incomplete_keeps_other_nans():
    df = messy()
    got = _f("drop_incomplete")(df, ["grade"])
    assert len(got) == 3
    assert got["name"].isna().sum() == 1, "only `required` columns decide which rows go"
    assert df["grade"].isna().sum() == 1, "the input DataFrame must not be modified"


def test_coerce_numeric():
    df = pd.DataFrame({"raw": ["1.5", "2", "oops", "4"], "tag": list("abcd")})
    got = _f("coerce_numeric")(df, "raw")
    assert got["raw"].dtype.kind == "f", "coerced column must be a float dtype"
    assert got["raw"].isna().tolist() == [False, False, True, False]
    assert got["raw"].dropna().tolist() == pytest.approx([1.5, 2.0, 4.0])
    assert got["tag"].tolist() == list("abcd")


def test_coerce_numeric_does_not_mutate():
    df = pd.DataFrame({"raw": ["1", "nope"]})
    _f("coerce_numeric")(df, "raw")
    assert df["raw"].tolist() == ["1", "nope"], "the input DataFrame must not be modified"
