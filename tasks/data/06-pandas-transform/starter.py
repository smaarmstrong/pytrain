import pandas as pd


def in_stock(df):
    """Rows with qty > 0, index reset. Never mutate df."""
    raise NotImplementedError


def top_n_by(df, col, n):
    """n rows with the largest `col`, sorted descending, index reset."""
    raise NotImplementedError


def with_total(df):
    """Copy of df plus a 'total' column (qty * price) as the last column."""
    raise NotImplementedError
