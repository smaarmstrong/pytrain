"""Cleaning layer: pandas transforms per the spec, in spec order."""
import pandas as pd


def clean(df):
    df = df.copy()
    # 1. strip product, drop missing/empty
    df["product"] = df["product"].astype("string").str.strip()
    df = df[df["product"].notna() & (df["product"] != "")]
    # 2. numeric coercion; drop non-numeric and quantity <= 0
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["quantity", "unit_price"])
    df = df[df["quantity"] > 0]
    # 3. dedupe order_id, first wins
    df = df.drop_duplicates(subset="order_id", keep="first")
    # 4./5. integer quantity, revenue column, original order
    df["quantity"] = df["quantity"].astype(int)
    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    return df.reset_index(drop=True)
