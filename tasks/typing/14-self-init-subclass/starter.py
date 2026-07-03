from typing import Any, ClassVar, Self


class QueryBuilder:
    def __init__(self, table):
        raise NotImplementedError

    def where(self, cond):
        raise NotImplementedError

    def limit(self, n):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError


class Plugin:
    registry: ClassVar[dict[str, type]] = {}

    # TODO: __init_subclass__(cls, *, name=None, **kwargs)
