import polars as pl


def top_categories_query(lf, n):
    return (
        lf.filter(pl.col("qty") > 0)
        .group_by("category")
        .agg((pl.col("qty") * pl.col("price")).sum().alias("revenue"))
        .sort("revenue", descending=True)
        .head(n)
    )


def top_categories(lf, n):
    return top_categories_query(lf, n).collect()
