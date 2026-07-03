# matplotlib: a figure to spec

In `solution.py`, implement one function. It is graded headlessly — build
and **return** the Figure; never call `plt.show()`.

```python
def make_figure(x, y):
    """Return a matplotlib Figure containing exactly one Axes with:

    - a line plot of y against x (the given sequences of numbers),
      the line labelled "signal"
    - title:   "Signal over time"
    - x-label: "t"
    - y-label: "value"
    - a visible legend (showing the "signal" entry)
    """
```

The grader inspects the returned Figure object graph — `fig.axes`, the
axes' `get_title()`/`get_xlabel()`/`get_ylabel()`, the line's
`get_xdata()`/`get_ydata()`, and the legend — so build exactly what the
spec says, on the figure you return.

Example:

```python
>>> fig = make_figure([0, 1, 2], [3.0, 1.0, 2.0])
>>> len(fig.axes)
1
>>> fig.axes[0].get_title()
'Signal over time'
```
