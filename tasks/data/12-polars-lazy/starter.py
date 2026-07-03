import polars as pl


def top_categories_query(lf, n):
    """Build the lazy query (filter -> group -> sort -> head) WITHOUT running it."""
    raise NotImplementedError


def top_categories(lf, n):
    """Collect the query into a pl.DataFrame."""
    raise NotImplementedError
