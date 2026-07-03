from typing import TypeGuard


def is_str_list(items: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in items)


def join_upper(items: list[object]) -> str:
    if is_str_list(items):
        return "-".join(item.upper() for item in items)
    raise TypeError("join_upper needs a list of strings")


def describe(value: int | str | list[object]) -> str:
    if isinstance(value, int):
        return f"number {value}"
    if isinstance(value, str):
        return f"text {value}"
    return f"list of {len(value)} items"
