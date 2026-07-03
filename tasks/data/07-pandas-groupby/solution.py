def region_summary(df):
    return (
        df.groupby("region")
        .agg(
            total_units=("units", "sum"),
            total_revenue=("revenue", "sum"),
            avg_units=("units", "mean"),
        )
        .reset_index()
        .sort_values("region")
        .reset_index(drop=True)
    )


def top_region(df):
    return df.groupby("region")["revenue"].sum().idxmax()


def product_units(df):
    return {k: int(v) for k, v in df.groupby("product")["units"].sum().items()}
