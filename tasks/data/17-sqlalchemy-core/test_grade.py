import pytest
import sqlalchemy as sa

from pytrain_grader import load_solution, get_attr


def _mod():
    return load_solution()


def fresh_db():
    mod = _mod()
    engine = get_attr(mod, "make_engine")()
    table = get_attr(mod, "build_schema")(engine)
    return mod, engine, table


ROWS = [
    {"name": "bolt", "price": 0.1},
    {"name": "anvil", "price": 99.5},
    {"name": "bracket", "price": 3.75},
    {"name": "apple", "price": 0.4},
]


def test_engine_is_in_memory_sqlite():
    engine = get_attr(_mod(), "make_engine")()
    assert isinstance(engine, sa.engine.Engine), "make_engine must return an Engine"
    assert engine.url.get_backend_name() == "sqlite"
    assert engine.url.database in (None, ":memory:"), "the database must be in-memory"


def test_schema_creates_products_table():
    _, engine, table = fresh_db()
    insp = sa.inspect(engine)
    assert "products" in insp.get_table_names()
    cols = {c["name"] for c in insp.get_columns("products")}
    assert cols == {"id", "name", "price"}
    assert isinstance(table, sa.Table), "build_schema must return the Table object"
    pk = insp.get_pk_constraint("products")["constrained_columns"]
    assert pk == ["id"]


def test_insert_persists_rows():
    mod, engine, table = fresh_db()
    get_attr(mod, "insert_rows")(engine, table, ROWS)
    with engine.connect() as conn:
        count = conn.execute(sa.select(sa.func.count()).select_from(table)).scalar()
        assert count == 4
        prices = dict(conn.execute(sa.select(table.c.name, table.c.price)).all())
    assert prices["anvil"] == pytest.approx(99.5)
    assert prices["bolt"] == pytest.approx(0.1)


def test_ids_autogenerate():
    mod, engine, table = fresh_db()
    get_attr(mod, "insert_rows")(engine, table, ROWS)
    with engine.connect() as conn:
        ids = [row[0] for row in conn.execute(sa.select(table.c.id))]
    assert len(ids) == 4
    assert all(i is not None for i in ids)
    assert len(set(ids)) == 4


def test_names_cheaper_than_sorted():
    mod, engine, table = fresh_db()
    get_attr(mod, "insert_rows")(engine, table, ROWS)
    got = get_attr(mod, "names_cheaper_than")(engine, table, 5.0)
    assert got == ["apple", "bolt", "bracket"]
    assert all(isinstance(n, str) for n in got)


def test_names_cheaper_than_boundary_exclusive():
    mod, engine, table = fresh_db()
    get_attr(mod, "insert_rows")(engine, table, ROWS)
    assert get_attr(mod, "names_cheaper_than")(engine, table, 0.1) == []


def test_names_cheaper_than_empty_table():
    mod, engine, table = fresh_db()
    assert get_attr(mod, "names_cheaper_than")(engine, table, 100.0) == []
