"""Auth layer (suggested split): the X-API-Key header dependency."""

API_KEY = "sekrit-123"


def require_api_key():
    """FastAPI dependency: 401 {"detail": "invalid API key"} unless the
    X-API-Key request header equals API_KEY.

    Hint: declare the header with `x_api_key: str | None = Header(default=None)`
    and raise HTTPException on mismatch.
    """
    raise NotImplementedError
