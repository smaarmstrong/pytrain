"""Grades the sales pipeline end-to-end: runs pipeline.py as a subprocess on
a grader-written messy CSV, then inspects the SQLite file and stdout."""
import sqlite3

import pytest

from pytrain_grader import run_solution

CSV = """\
order_id,date,product,quantity,unit_price
1,2026-01-05,Widget,3,2.50
2,2026-01-05, Widget ,1,2.50
3,2026-01-06,Gadget,2,4.00
4,2026-01-06,,5,1.00
5,2026-01-07,Gizmo,two,3.00
3,2026-01-08,Gadget,9,4.00
6,2026-01-08,Gizmo,4,1.25
7,2026-01-09,Widget,0,2.50
8,2026-01-09,Gadget,1,4.00
"""
# survivors: order_id 1, 2 (product stripped), 3 (first), 6, 8
# dropped: 4 (no product), 5 (bad qty), dup 3, 7 (qty 0)

EXPECTED_STDOUT = [
    "Gadget: qty=3 revenue=12.00",
    "Gizmo: qty=4 revenue=5.00",
    "Widget: qty=4 revenue=10.00",
    "TOTAL revenue=27.00",
]


@pytest.fixture()
def paths(tmp_path):
    csv = tmp_path / "sales.csv"
    csv.write_text(CSV, encoding="utf-8")
    return csv, tmp_path / "sales.db"


def pipeline(csv, db):
    return run_solution(str(csv), str(db), filename="pipeline.py")


def rows(db, query):
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in con.execute(query).fetchall()]
    finally:
        con.close()


def test_runs_ok_and_prints_report(paths):
    csv, db = paths
    r = pipeline(csv, db)
    assert r.returncode == 0, r.stderr
    assert r.stdout.splitlines() == EXPECTED_STDOUT


def test_sales_table_cleaned(paths):
    csv, db = paths
    pipeline(csv, db)
    got = rows(db, "SELECT * FROM sales")
    assert len(got) == 5
    assert set(got[0].keys()) == {
        "order_id", "date", "product", "quantity", "unit_price", "revenue",
    }
    assert [g["order_id"] for g in got] == [1, 2, 3, 6, 8]  # original order, dedup first-wins
    by_id = {g["order_id"]: g for g in got}
    assert by_id[2]["product"] == "Widget"  # whitespace stripped
    assert by_id[1]["quantity"] == 3
    assert by_id[1]["revenue"] == pytest.approx(7.50)
    assert by_id[6]["unit_price"] == pytest.approx(1.25)
    assert by_id[6]["revenue"] == pytest.approx(5.00)
    assert by_id[3]["quantity"] == 2  # the first order_id 3, not the duplicate


def test_summary_table(paths):
    csv, db = paths
    pipeline(csv, db)
    got = rows(db, "SELECT * FROM summary")
    assert [g["product"] for g in got] == ["Gadget", "Gizmo", "Widget"]  # asc
    assert set(got[0].keys()) == {"product", "total_qty", "total_revenue"}
    assert [g["total_qty"] for g in got] == [3, 4, 4]
    assert [g["total_revenue"] for g in got] == [
        pytest.approx(12.00), pytest.approx(5.00), pytest.approx(10.00),
    ]


def test_rerun_replaces_not_appends(paths):
    csv, db = paths
    pipeline(csv, db)
    r = pipeline(csv, db)
    assert r.returncode == 0
    assert len(rows(db, "SELECT * FROM sales")) == 5
    assert len(rows(db, "SELECT * FROM summary")) == 3
    assert r.stdout.splitlines() == EXPECTED_STDOUT


def test_all_rows_clean_passthrough(tmp_path):
    csv = tmp_path / "ok.csv"
    csv.write_text(
        "order_id,date,product,quantity,unit_price\n"
        "10,2026-02-01,Anvil,2,10.00\n",
        encoding="utf-8",
    )
    db = tmp_path / "ok.db"
    r = pipeline(csv, db)
    assert r.returncode == 0
    assert r.stdout.splitlines() == [
        "Anvil: qty=2 revenue=20.00",
        "TOTAL revenue=20.00",
    ]
    got = rows(db, "SELECT * FROM sales")
    assert len(got) == 1
    assert got[0]["revenue"] == pytest.approx(20.00)


def test_missing_csv_errors_and_no_db(tmp_path):
    csv = tmp_path / "gone.csv"
    db = tmp_path / "out.db"
    r = pipeline(csv, db)
    assert r.returncode == 1
    assert r.stdout == ""
    assert r.stderr.rstrip("\n") == f"error: no such file: {csv}"
    assert not db.exists()
