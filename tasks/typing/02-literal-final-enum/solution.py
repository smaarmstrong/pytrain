import enum
from typing import Final, Literal

MAX_RETRIES: Final[int] = 3


class Status(enum.Enum):
    OK = "ok"
    WARN = "warn"
    ERROR = "error"


def set_mode(mode: Literal["r", "w", "a"]) -> str:
    if mode not in ("r", "w", "a"):
        raise ValueError(f"unsupported mode: {mode!r}")
    return f"mode set to {mode}"


def severity(status: Status) -> int:
    return {Status.OK: 0, Status.WARN: 1, Status.ERROR: 2}[status]
