import httpx


class APIClient:
    """A small API client with retries — see prompt.md."""

    def __init__(self, base_url, *, transport=None, max_retries=3,
                 timeout=1.0, backoff=0.0):
        ...

    def get_json(self, path):
        ...

    def close(self):
        ...
