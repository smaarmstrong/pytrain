"""sales pipeline: CSV -> pandas clean -> SQLite + summary report."""
import argparse
import sqlite3
import sys
from pathlib import Path

import pandas as pd

from clean import clean


def main(argv=None):
    ap = argparse.ArgumentParser(prog="pipeline")
    ap.add_argument("input_csv")
    ap.add_argument("output_db")
    args = ap.parse_args(argv)

    src = Path(args.input_csv)
    if not src.is_file():
        print(f"error: no such file: {args.input_csv}", file=sys.stderr)
        return 1

    df = clean(pd.read_csv(src))

    summary = (
        df.groupby("product", as_index=False)
        .agg(total_qty=("quantity", "sum"), total_revenue=("revenue", "sum"))
        .sort_values("product")
        .reset_index(drop=True)
    )
    summary["total_revenue"] = summary["total_revenue"].round(2)

    con = sqlite3.connect(args.output_db)
    try:
        df[["order_id", "date", "product", "quantity", "unit_price", "revenue"]].to_sql(
            "sales", con, index=False, if_exists="replace"
        )
        summary.to_sql("summary", con, index=False, if_exists="replace")
    finally:
        con.close()

    for row in summary.itertuples(index=False):
        print(f"{row.product}: qty={int(row.total_qty)} revenue={row.total_revenue:.2f}")
    print(f"TOTAL revenue={summary['total_revenue'].sum():.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
