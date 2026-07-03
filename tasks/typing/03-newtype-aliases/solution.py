from typing import NewType, TypeAlias

UserId = NewType("UserId", int)

# On 3.12+ you'd write:  type Vector = list[float]
Vector: TypeAlias = list[float]


def make_user_id(raw: int) -> UserId:
    if raw <= 0:
        raise ValueError(f"user ids must be positive, got {raw}")
    return UserId(raw)


def scale(v: Vector, k: float) -> Vector:
    return [x * k for x in v]


def lookup(names: dict[UserId, str], uid: UserId) -> str | None:
    return names.get(uid)
