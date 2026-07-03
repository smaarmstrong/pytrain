import pandas as pd


def missing_counts(df):
    """{column: missing count} as plain ints."""
    raise NotImplementedError


def fill_defaults(df, defaults):
    """Copy of df with NaNs filled per-column from `defaults`."""
    raise NotImplementedError


def drop_incomplete(df, required):
    """Only rows with values in every `required` column."""
    raise NotImplementedError


def coerce_numeric(df, col):
    """Copy of df with `col` coerced to floats (bad entries -> NaN)."""
    raise NotImplementedError
