class Query:
    def __init__(self, table):
        self._table = table
        self._columns = []
        self._conditions = []
        self._order = None  # (column, desc)
        self._limit = None

    def select(self, *columns):
        self._columns.extend(columns)
        return self

    def where(self, condition):
        self._conditions.append(condition)
        return self

    def order_by(self, column, desc=False):
        self._order = (column, desc)
        return self

    def limit(self, n):
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            raise ValueError("limit must be a non-negative integer")
        self._limit = n
        return self

    def build(self):
        columns = ", ".join(self._columns) if self._columns else "*"
        parts = [f"SELECT {columns} FROM {self._table}"]
        if self._conditions:
            parts.append("WHERE " + " AND ".join(self._conditions))
        if self._order is not None:
            column, desc = self._order
            parts.append(f"ORDER BY {column}" + (" DESC" if desc else ""))
        if self._limit is not None:
            parts.append(f"LIMIT {self._limit}")
        return " ".join(parts)
