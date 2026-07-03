"""A correct implementation of the spec in prompt.md — write tests for it."""


def fetch(url):
    """Pretend network call — never callable outside production."""
    raise RuntimeError("network access is disabled here — patch me in tests")


def fetch_with_retry(url, attempts=3):
    last = None
    for _ in range(attempts):
        try:
            return fetch(url)
        except ConnectionError as exc:
            last = exc
    raise last
