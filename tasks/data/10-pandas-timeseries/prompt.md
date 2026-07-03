# pandas: resample & rolling

In `solution.py` (with `import pandas as pd`), implement three functions.
Each receives a `pd.Series` of floats whose index is a `DatetimeIndex`
(timestamps at arbitrary times of day, in ascending order).

```python
def daily_totals(s):
    """Resample to calendar days: a Series indexed by day (midnight
    timestamps) whose values are the SUM of that day's entries.

    Days between the first and last observation that have no entries must
    still appear, with total 0.0 (that's resample semantics — a plain
    groupby-by-date would drop them)."""

def rolling_mean(s, window):
    """The rolling mean of s over `window` observations: entry i is the
    mean of entries i-window+1 .. i. The first window-1 entries are NaN.
    Same index as s."""

def busiest_day(s):
    """The calendar day with the largest daily total, as an ISO date
    string like "2024-01-03". No ties in graded data."""
```

Example:

```python
>>> idx = pd.to_datetime(["2024-01-01 09:00", "2024-01-01 15:00", "2024-01-03 08:00"])
>>> s = pd.Series([2.0, 3.0, 4.0], index=idx)
>>> daily_totals(s).tolist()       # 2024-01-02 present as 0.0
[5.0, 0.0, 4.0]
>>> busiest_day(s)
'2024-01-01'
```
