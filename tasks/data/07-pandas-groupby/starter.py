import pandas as pd


def region_summary(df):
    """Per-region named aggregations: total_units, total_revenue, avg_units."""
    raise NotImplementedError


def top_region(df):
    """Region with the highest total revenue."""
    raise NotImplementedError


def product_units(df):
    """dict: product -> total units."""
    raise NotImplementedError
