from enum import Flag, IntEnum, StrEnum, auto


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Color(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


def parse_permissions(names):
    result = Permission(0)
    for name in names:
        try:
            result |= Permission[name.upper()]
        except KeyError:
            raise ValueError(f"unknown permission: {name!r}") from None
    return result
