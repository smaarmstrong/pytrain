import enum
from typing import Final, Literal

# TODO: MAX_RETRIES, annotated Final[int], value 3


class Status(enum.Enum):
    """TODO: members OK, WARN, ERROR with values 'ok', 'warn', 'error'."""


def set_mode(mode):
    raise NotImplementedError


def severity(status):
    raise NotImplementedError
