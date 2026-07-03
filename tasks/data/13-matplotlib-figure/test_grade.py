import matplotlib

matplotlib.use("Agg")  # headless — must run before any pyplot import anywhere

import pytest
from matplotlib.figure import Figure

from pytrain_grader import load_solution, get_attr

X = [0, 1, 2, 3, 4]
Y = [3.0, 1.5, 4.0, 2.0, 5.5]


def make():
    return get_attr(load_solution(), "make_figure")(X, Y)


def test_returns_figure_with_one_axes():
    fig = make()
    assert isinstance(fig, Figure)
    assert len(fig.axes) == 1


def test_line_data():
    ax = make().axes[0]
    lines = ax.get_lines()
    assert len(lines) >= 1, "the Axes must contain a line plot"
    line = lines[0]
    assert list(line.get_xdata()) == pytest.approx(X)
    assert list(line.get_ydata()) == pytest.approx(Y)


def test_line_data_other_input():
    fig = get_attr(load_solution(), "make_figure")([10, 20], [-1.0, 1.0])
    line = fig.axes[0].get_lines()[0]
    assert list(line.get_xdata()) == pytest.approx([10, 20])
    assert list(line.get_ydata()) == pytest.approx([-1.0, 1.0])


def test_title_and_labels():
    ax = make().axes[0]
    assert ax.get_title() == "Signal over time"
    assert ax.get_xlabel() == "t"
    assert ax.get_ylabel() == "value"


def test_legend_present_with_signal_entry():
    ax = make().axes[0]
    legend = ax.get_legend()
    assert legend is not None, "call ax.legend() so the legend is shown"
    texts = [t.get_text() for t in legend.get_texts()]
    assert "signal" in texts
