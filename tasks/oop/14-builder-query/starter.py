class Query:
    """Fluent builder: select/where/order_by/limit chain, build() -> str.

    See prompt.md for the exact output format and error cases.
    """

    def __init__(self, table):
        raise NotImplementedError

    def select(self, *columns):
        raise NotImplementedError

    def where(self, condition):
        raise NotImplementedError

    def order_by(self, column, desc=False):
        raise NotImplementedError

    def limit(self, n):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError
