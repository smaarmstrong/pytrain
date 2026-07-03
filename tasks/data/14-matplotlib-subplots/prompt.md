# matplotlib: two-panel dashboard

In `solution.py`, implement one function. Graded headlessly — build and
**return** the Figure; never call `plt.show()`.

```python
def make_dashboard(x, trend, volume):
    """Return a Figure with exactly two Axes stacked vertically
    (2 rows x 1 column — e.g. plt.subplots(2, 1)).

    Top panel ("Trend"):
      - line plot of `trend` against `x`
      - title "Trend", y-label "level"

    Bottom panel ("Volume"):
      - BAR chart of `volume` against `x` (one bar per x value)
      - title "Volume", y-label "count"

    `x`, `trend` and `volume` are equal-length sequences of numbers.
    """
```

The grader finds each panel by its title, then asserts the line's
x/y data on the trend panel and the bar heights on the volume panel, all
from the returned Figure's object graph.

Example:

```python
>>> fig = make_dashboard([0, 1], [2.0, 3.0], [5, 1])
>>> sorted(ax.get_title() for ax in fig.axes)
['Trend', 'Volume']
```
