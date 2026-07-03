"""Small config helpers, fully annotated."""


def parse_port(value: str) -> int | None:
    try:
        port = int(value.strip())
    except ValueError:
        return None
    if 0 <= port <= 65535:
        return port
    return None


def normalize_host(host: str | None) -> str:
    if host is None or not host.strip():
        return "localhost"
    return host.strip().lower()


def get_flag(settings: dict[str, str], name: str, default: bool = False) -> bool:
    raw = settings.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def summarize(settings: dict[str, str]) -> str:
    parts = []
    for key in sorted(settings):
        parts.append(f"{key}={settings[key]}")
    return ", ".join(parts)
