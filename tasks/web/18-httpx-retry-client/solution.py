import time

import httpx


class APIClient:
    def __init__(self, base_url, *, transport=None, max_retries=3,
                 timeout=1.0, backoff=0.0):
        self.max_retries = max_retries
        self.backoff = backoff
        kwargs = {"base_url": base_url, "timeout": timeout}
        if transport is not None:
            kwargs["transport"] = transport
        self._client = httpx.Client(**kwargs)

    def get_json(self, path):
        last_error = None
        for attempt in range(self.max_retries + 1):
            if attempt and self.backoff:
                time.sleep(self.backoff * 2 ** (attempt - 1))
            try:
                r = self._client.get(path)
                r.raise_for_status()
                return r.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code < 500:
                    raise  # 4xx: our fault, retrying won't help
                last_error = e
            except httpx.TransportError as e:
                last_error = e
        raise last_error

    def close(self):
        self._client.close()
