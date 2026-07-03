import pandas as pd


def make_inventory():
    """The exact 4-row inventory DataFrame from the prompt."""
    raise NotImplementedError


def first_n_names(df, n):
    """First n values of the 'name' column as a Python list."""
    raise NotImplementedError


def row_by_sku(df, sku):
    """The row with that sku, as a plain dict."""
    raise NotImplementedError


def numeric_summary(df):
    """{"total_qty": ..., "max_price": ...}."""
    raise NotImplementedError
