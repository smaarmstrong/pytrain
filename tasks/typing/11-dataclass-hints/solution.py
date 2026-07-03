from dataclasses import dataclass, field, fields
from typing import Any, get_type_hints


@dataclass
class Task:
    title: str
    priority: int = 1
    tags: list[str] = field(default_factory=list)
    done: bool = False


def field_types(cls: type) -> dict[str, type]:
    return get_type_hints(cls)


def mismatched_fields(obj: Any) -> list[str]:
    hints = get_type_hints(type(obj))
    bad = []
    for f in fields(obj):
        hint = hints.get(f.name)
        if isinstance(hint, type) and not isinstance(getattr(obj, f.name), hint):
            bad.append(f.name)
    return sorted(bad)
