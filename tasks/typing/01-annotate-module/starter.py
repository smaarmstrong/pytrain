"""Small config helpers. They work — but nothing is annotated yet.

Annotate every function (params and returns) per prompt.md. Don't change
behaviour.
"""


def parse_port(value):
    try:
        port = int(value.strip())
    except ValueError:
        return None
    if 0 <= port <= 65535:
        return port
    return None


def normalize_host(host):
    if host is None or not host.strip():
        return "localhost"
    return host.strip().lower()


def get_flag(settings, name, default=False):
    raw = settings.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def summarize(settings):
    parts = []
    for key in sorted(settings):
        parts.append(f"{key}={settings[key]}")
    return ", ".join(parts)
