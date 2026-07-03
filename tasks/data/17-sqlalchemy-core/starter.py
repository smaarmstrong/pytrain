import sqlalchemy as sa


def make_engine():
    """Engine for an in-memory SQLite database."""
    raise NotImplementedError


def build_schema(engine):
    """Create the 'products' table (id pk, name str, price float); return the Table."""
    raise NotImplementedError


def insert_rows(engine, table, rows):
    """Insert a list of {"name": ..., "price": ...} dicts and commit."""
    raise NotImplementedError


def names_cheaper_than(engine, table, max_price):
    """Names with price < max_price, sorted, as list[str]."""
    raise NotImplementedError
