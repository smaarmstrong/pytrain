def load_sales(csv_path):
    """CSV -> in-memory sqlite3 with a typed `sales` table; return the Connection."""
    raise NotImplementedError


def total_revenue(conn):
    """SUM(units * price) over all rows, as a float."""
    raise NotImplementedError


def units_by_region(conn):
    """{region: total units} for every region in the table."""
    raise NotImplementedError


def top_product(conn):
    """Product with the highest total revenue."""
    raise NotImplementedError
