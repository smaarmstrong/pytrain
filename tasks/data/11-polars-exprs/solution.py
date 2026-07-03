import polars as pl


def select_cols(df, cols):
    return df.select(cols)


def filter_at_least(df, min_qty):
    return df.filter(pl.col("qty") >= min_qty)


def add_revenue(df):
    return df.with_columns((pl.col("qty") * pl.col("price")).alias("revenue"))


def category_totals(df):
    return (
        df.group_by("category")
        .agg(pl.col("qty").sum().alias("total_qty"))
        .sort("category")
    )
