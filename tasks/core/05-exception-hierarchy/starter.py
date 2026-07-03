class ConfigError(Exception):
    """Base class for configuration problems."""


class MissingKeyError(ConfigError):
    """A required key was absent."""


class InvalidValueError(ConfigError):
    """A value failed to parse or was out of range."""


def parse_port(raw) -> int:
    """int in 1..65535; InvalidValueError otherwise (chained on parse failure)."""
    raise NotImplementedError


def get_port(config: dict, log: list) -> int:
    """See prompt.md for the exact audit-log protocol (else/finally)."""
    raise NotImplementedError
