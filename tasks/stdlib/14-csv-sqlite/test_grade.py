import sqlite3

import pytest

from pytrain_grader import load_solution, get_attr

CSV = """region,product,units,price
north,widget,10,2.50
north,gadget,2,10.00
south,gadget,3,10.00
south,widget,4,2.50
east,doohickey,1,99.00
"""
# revenue: widget 25+10=35, gadget 20+30=50, doohickey 99 -> total 184.0


def make_csv(tmp_path, text=CSV):
    p = tmp_path / "sales.csv"
    p.write_text(text, encoding="utf-8")
    return p


def test_load_returns_connection_with_sales_table(tmp_path):
    load_sales = get_attr(load_solution(), "load_sales")
    conn = load_sales(make_csv(tmp_path))
    assert isinstance(conn, sqlite3.Connection)
    assert conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 5


def test_columns_are_typed_not_strings(tmp_path):
    load_sales = get_attr(load_solution(), "load_sales")
    conn = load_sales(make_csv(tmp_path))
    units, price = conn.execute(
        "SELECT units, price FROM sales WHERE product = 'doohickey'"
    ).fetchone()
    assert units == 1 and isinstance(units, int)
    assert price == pytest.approx(99.0) and isinstance(price, float)
    # numeric SUM must work (would concatenate/fail on TEXT-typed data)
    assert conn.execute("SELECT SUM(units) FROM sales").fetchone()[0] == 20


def test_rows_loaded_faithfully(tmp_path):
    load_sales = get_attr(load_solution(), "load_sales")
    conn = load_sales(make_csv(tmp_path))
    rows = conn.execute(
        "SELECT region, product, units FROM sales ORDER BY region, product"
    ).fetchall()
    assert rows == [
        ("east", "doohickey", 1),
        ("north", "gadget", 2),
        ("north", "widget", 10),
        ("south", "gadget", 3),
        ("south", "widget", 4),
    ]


def test_total_revenue(tmp_path):
    mod = load_solution()
    conn = get_attr(mod, "load_sales")(make_csv(tmp_path))
    assert get_attr(mod, "total_revenue")(conn) == pytest.approx(184.0)


def test_total_revenue_empty_table(tmp_path):
    mod = load_solution()
    conn = get_attr(mod, "load_sales")(make_csv(tmp_path, "region,product,units,price\n"))
    assert get_attr(mod, "total_revenue")(conn) == pytest.approx(0.0)


def test_units_by_region(tmp_path):
    mod = load_solution()
    conn = get_attr(mod, "load_sales")(make_csv(tmp_path))
    assert get_attr(mod, "units_by_region")(conn) == {"north": 12, "south": 7, "east": 1}


def test_top_product(tmp_path):
    mod = load_solution()
    conn = get_attr(mod, "load_sales")(make_csv(tmp_path))
    assert get_attr(mod, "top_product")(conn) == "doohickey"


def test_query_functions_work_on_a_foreign_connection(tmp_path):
    mod = load_solution()
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE sales (region TEXT, product TEXT, units INTEGER, price REAL)"
    )
    conn.executemany(
        "INSERT INTO sales VALUES (?, ?, ?, ?)",
        [("west", "cog", 5, 2.0), ("west", "cam", 1, 100.0)],
    )
    assert get_attr(mod, "total_revenue")(conn) == pytest.approx(110.0)
    assert get_attr(mod, "units_by_region")(conn) == {"west": 6}
    assert get_attr(mod, "top_product")(conn) == "cam"
