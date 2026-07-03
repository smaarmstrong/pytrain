from collections.abc import Sequence


def pick[T](items: Sequence[T], index: int) -> T:
    return items[index]


def swap[A, B](pair: tuple[A, B]) -> tuple[B, A]:
    x, y = pair
    return (y, x)


class Pair[T]:
    def __init__(self, first: T, second: T) -> None:
        self.first = first
        self.second = second

    def swapped(self) -> "Pair[T]":
        return Pair(self.second, self.first)

    def as_tuple(self) -> tuple[T, T]:
        return (self.first, self.second)
