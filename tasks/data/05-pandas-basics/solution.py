import pandas as pd


def make_inventory():
    return pd.DataFrame(
        {
            "sku": ["A1", "A2", "B1", "B2"],
            "name": ["anvil", "apple", "bolt", "bracket"],
            "qty": [10, 40, 300, 25],
            "price": [99.5, 0.4, 0.1, 3.75],
        }
    )


def first_n_names(df, n):
    return df["name"].iloc[:n].tolist()


def row_by_sku(df, sku):
    row = df.loc[df["sku"] == sku].iloc[0]
    return {k: (v.item() if hasattr(v, "item") else v) for k, v in row.items()}


def numeric_summary(df):
    return {"total_qty": int(df["qty"].sum()), "max_price": float(df["price"].max())}
