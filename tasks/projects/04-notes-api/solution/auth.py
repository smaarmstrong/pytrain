"""Auth layer: the X-API-Key header dependency."""
from fastapi import Header, HTTPException

API_KEY = "sekrit-123"


def require_api_key(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid API key")
