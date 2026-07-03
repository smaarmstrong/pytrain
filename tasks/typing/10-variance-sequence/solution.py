from collections.abc import Sequence
from typing import Generic, TypeVar

T_co = TypeVar("T_co", covariant=True)


class Box(Generic[T_co]):
    def __init__(self, value: T_co) -> None:
        self._value = value

    def get(self) -> T_co:
        return self._value


def total(nums: Sequence[float]) -> float:
    return sum(nums)


def labels_upper(labels: Sequence[str]) -> list[str]:
    return [label.upper() for label in labels]
