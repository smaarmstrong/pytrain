import csv
import sqlite3
from pathlib import Path


def load_sales(csv_path):
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE sales (region TEXT, product TEXT, units INTEGER, price REAL)"
    )
    with Path(csv_path).open(newline="", encoding="utf-8") as f:
        rows = [
            (r["region"], r["product"], int(r["units"]), float(r["price"]))
            for r in csv.DictReader(f)
        ]
    conn.executemany("INSERT INTO sales VALUES (?, ?, ?, ?)", rows)
    conn.commit()
    return conn


def total_revenue(conn):
    (total,) = conn.execute("SELECT COALESCE(SUM(units * price), 0) FROM sales").fetchone()
    return float(total)


def units_by_region(conn):
    rows = conn.execute("SELECT region, SUM(units) FROM sales GROUP BY region")
    return {region: units for region, units in rows}


def top_product(conn):
    row = conn.execute(
        "SELECT product FROM sales GROUP BY product "
        "ORDER BY SUM(units * price) DESC LIMIT 1"
    ).fetchone()
    return row[0]
