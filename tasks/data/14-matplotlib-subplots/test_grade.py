import matplotlib

matplotlib.use("Agg")  # headless — must run before any pyplot import anywhere

import pytest
from matplotlib.figure import Figure

from pytrain_grader import load_solution, get_attr

X = [0, 1, 2, 3]
TREND = [1.0, 2.5, 2.0, 4.0]
VOLUME = [7, 3, 5, 1]


def dashboard():
    return get_attr(load_solution(), "make_dashboard")(X, TREND, VOLUME)


def _panel(fig, title):
    hits = [ax for ax in fig.axes if ax.get_title() == title]
    assert hits, f"no Axes titled {title!r} found on the figure"
    return hits[0]


def test_two_axes_stacked_vertically():
    fig = dashboard()
    assert isinstance(fig, Figure)
    assert len(fig.axes) == 2
    boxes = sorted((ax.get_position() for ax in fig.axes), key=lambda b: -b.y0)
    assert boxes[0].y0 > boxes[1].y0, "panels must be stacked (2 rows, 1 column)"
    xs = [round(ax.get_position().x0, 3) for ax in fig.axes]
    assert xs[0] == xs[1], "panels must be in a single column"


def test_titles():
    fig = dashboard()
    assert sorted(ax.get_title() for ax in fig.axes) == ["Trend", "Volume"]


def test_trend_panel_line_data():
    ax = _panel(dashboard(), "Trend")
    lines = ax.get_lines()
    assert len(lines) >= 1, "the Trend panel must contain a line plot"
    assert list(lines[0].get_xdata()) == pytest.approx(X)
    assert list(lines[0].get_ydata()) == pytest.approx(TREND)
    assert ax.get_ylabel() == "level"


def test_volume_panel_bars():
    ax = _panel(dashboard(), "Volume")
    bars = ax.patches
    assert len(bars) == len(X), "one bar per x value on the Volume panel"
    heights = sorted(p.get_height() for p in bars)
    assert heights == pytest.approx(sorted(VOLUME))
    assert ax.get_ylabel() == "count"


def test_other_input_flows_through():
    fig = get_attr(load_solution(), "make_dashboard")([0, 1], [9.0, 8.0], [2, 4])
    trend_ax = _panel(fig, "Trend")
    assert list(trend_ax.get_lines()[0].get_ydata()) == pytest.approx([9.0, 8.0])
    vol_ax = _panel(fig, "Volume")
    assert sorted(p.get_height() for p in vol_ax.patches) == pytest.approx([2, 4])
