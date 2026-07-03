import polars as pl


def select_cols(df, cols):
    """Only the named columns, in order."""
    raise NotImplementedError


def filter_at_least(df, min_qty):
    """Rows with qty >= min_qty."""
    raise NotImplementedError


def add_revenue(df):
    """Add 'revenue' = qty * price."""
    raise NotImplementedError


def category_totals(df):
    """Per-category qty sums as 'total_qty', sorted by category."""
    raise NotImplementedError
