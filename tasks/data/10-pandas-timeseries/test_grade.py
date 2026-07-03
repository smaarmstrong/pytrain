import math

import pandas as pd
import pytest

from pytrain_grader import load_solution, get_attr


def _f(name):
    return get_attr(load_solution(), name)


def series():
    idx = pd.to_datetime(
        [
            "2024-01-01 09:00",
            "2024-01-01 15:30",
            "2024-01-02 10:00",
            "2024-01-03 08:00",
            "2024-01-03 12:00",
            "2024-01-03 18:45",
        ]
    )
    return pd.Series([2.0, 3.0, 4.0, 1.0, 1.0, 1.5], index=idx)


def gappy():
    idx = pd.to_datetime(["2024-02-01 06:00", "2024-02-01 21:00", "2024-02-04 12:00"])
    return pd.Series([1.0, 2.0, 7.0], index=idx)


def test_daily_totals_values():
    got = _f("daily_totals")(series())
    assert isinstance(got, pd.Series)
    assert got.tolist() == pytest.approx([5.0, 4.0, 3.5])


def test_daily_totals_index_is_days():
    got = _f("daily_totals")(series())
    dates = [ts.date().isoformat() for ts in got.index]
    assert dates == ["2024-01-01", "2024-01-02", "2024-01-03"]


def test_daily_totals_gap_days_present_as_zero():
    got = _f("daily_totals")(gappy())
    dates = [ts.date().isoformat() for ts in got.index]
    assert dates == ["2024-02-01", "2024-02-02", "2024-02-03", "2024-02-04"], (
        "days with no entries must still appear (resample, not groupby-date)"
    )
    assert got.tolist() == pytest.approx([3.0, 0.0, 0.0, 7.0])


def test_rolling_mean_values():
    got = _f("rolling_mean")(series(), 3)
    assert isinstance(got, pd.Series)
    assert len(got) == 6
    assert math.isnan(got.iloc[0]) and math.isnan(got.iloc[1])
    assert got.iloc[2:].tolist() == pytest.approx([3.0, 8 / 3, 2.0, 7 / 6])


def test_rolling_mean_keeps_index():
    s = series()
    got = _f("rolling_mean")(s, 2)
    assert list(got.index) == list(s.index)
    assert math.isnan(got.iloc[0])
    assert got.iloc[1] == pytest.approx(2.5)


def test_rolling_mean_window_one():
    s = series()
    got = _f("rolling_mean")(s, 1)
    assert got.tolist() == pytest.approx(s.tolist())


def test_busiest_day():
    assert _f("busiest_day")(series()) == "2024-01-01"
    assert _f("busiest_day")(gappy()) == "2024-02-04"


def test_busiest_day_returns_str():
    got = _f("busiest_day")(series())
    assert isinstance(got, str)
