from fastapi import Depends, FastAPI

app = FastAPI()

STORE: dict[str, float] = {}


def get_store() -> dict[str, float]:
    return STORE


# def list_params(q: str | None = None, limit: int = 5): ...

# POST /products, GET /products, GET /products/cheap — see prompt.md.
# Every endpoint takes the store via Depends(get_store).
