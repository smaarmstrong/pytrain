import pandas as pd


def daily_totals(s):
    """Per-calendar-day sums (gap days present as 0.0)."""
    raise NotImplementedError


def rolling_mean(s, window):
    """Rolling mean over `window` observations (first window-1 are NaN)."""
    raise NotImplementedError


def busiest_day(s):
    """ISO date string of the day with the largest total."""
    raise NotImplementedError
