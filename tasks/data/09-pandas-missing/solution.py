import pandas as pd


def missing_counts(df):
    return {col: int(df[col].isna().sum()) for col in df.columns}


def fill_defaults(df, defaults):
    return df.fillna(defaults)


def drop_incomplete(df, required):
    return df.dropna(subset=list(required))


def coerce_numeric(df, col):
    out = df.copy()
    out[col] = pd.to_numeric(out[col], errors="coerce")
    return out
