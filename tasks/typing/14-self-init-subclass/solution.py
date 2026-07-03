from typing import Any, ClassVar, Self


class QueryBuilder:
    def __init__(self, table: str) -> None:
        self._table = table
        self._conds: list[str] = []
        self._limit: int | None = None

    def where(self, cond: str) -> Self:
        self._conds.append(cond)
        return self

    def limit(self, n: int) -> Self:
        self._limit = n
        return self

    def build(self) -> str:
        sql = f"SELECT * FROM {self._table}"
        if self._conds:
            sql += " WHERE " + " AND ".join(self._conds)
        if self._limit is not None:
            sql += f" LIMIT {self._limit}"
        return sql


class Plugin:
    registry: ClassVar[dict[str, type]] = {}

    def __init_subclass__(cls, *, name: str | None = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        Plugin.registry[name or cls.__name__.lower()] = cls
