from typing import overload


@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
@overload
def double(x: list[int]) -> list[int]: ...


def double(x: int | str | list[int]) -> int | str | list[int]:
    if isinstance(x, list):
        return [item * 2 for item in x]
    return x * 2
