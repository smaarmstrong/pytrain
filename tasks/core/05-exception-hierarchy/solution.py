class ConfigError(Exception):
    """Base class for configuration problems."""


class MissingKeyError(ConfigError):
    """A required key was absent."""


class InvalidValueError(ConfigError):
    """A value failed to parse or was out of range."""


def parse_port(raw) -> int:
    try:
        port = int(raw)
    except (ValueError, TypeError) as e:
        raise InvalidValueError(f"not an integer: {raw!r}") from e
    if not 1 <= port <= 65535:
        raise InvalidValueError(f"port out of range: {port}")
    return port


def get_port(config: dict, log: list) -> int:
    try:
        try:
            raw = config["port"]
        except KeyError:
            log.append("missing")
            raise MissingKeyError("port") from None
        try:
            port = parse_port(raw)
        except InvalidValueError:
            log.append("invalid")
            raise
        else:
            log.append("ok")
            return port
    finally:
        log.append("done")
