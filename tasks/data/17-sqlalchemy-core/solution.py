import sqlalchemy as sa


def make_engine():
    return sa.create_engine("sqlite+pysqlite:///:memory:")


def build_schema(engine):
    metadata = sa.MetaData()
    products = sa.Table(
        "products",
        metadata,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
    )
    metadata.create_all(engine)
    return products


def insert_rows(engine, table, rows):
    with engine.begin() as conn:
        conn.execute(sa.insert(table), list(rows))


def names_cheaper_than(engine, table, max_price):
    stmt = (
        sa.select(table.c.name)
        .where(table.c.price < max_price)
        .order_by(table.c.name)
    )
    with engine.connect() as conn:
        return [row[0] for row in conn.execute(stmt)]
