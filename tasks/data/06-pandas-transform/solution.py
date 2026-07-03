def in_stock(df):
    return df[df["qty"] > 0].reset_index(drop=True)


def top_n_by(df, col, n):
    return df.sort_values(col, ascending=False).head(n).reset_index(drop=True)


def with_total(df):
    return df.assign(total=(df["qty"] * df["price"]).astype(float))
