from collections.abc import Iterable, Sequence
from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


def first(items: Sequence[T]) -> T:
    if not items:
        raise ValueError("empty sequence has no first element")
    return items[0]


def pairs(a: Iterable[T], b: Iterable[U]) -> list[tuple[T, U]]:
    return list(zip(a, b))


def dedupe(items: Iterable[T]) -> list[T]:
    seen: set[T] = set()
    out: list[T] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out
