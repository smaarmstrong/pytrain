import pandas as pd


def daily_totals(s):
    return s.resample("D").sum()


def rolling_mean(s, window):
    return s.rolling(window).mean()


def busiest_day(s):
    totals = daily_totals(s)
    return totals.idxmax().date().isoformat()
