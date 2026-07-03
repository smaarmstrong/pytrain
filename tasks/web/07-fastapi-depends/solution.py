from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

STORE: dict[str, float] = {}


def get_store() -> dict[str, float]:
    return STORE


class ListParams:
    def __init__(self, q: str | None = None, limit: int = 5):
        self.q = q
        self.limit = limit


def list_params(q: str | None = None, limit: int = 5) -> ListParams:
    return ListParams(q=q, limit=limit)


class ProductIn(BaseModel):
    name: str
    price: float


@app.post("/products", status_code=201)
def create_product(product: ProductIn, store: dict = Depends(get_store)):
    if product.name in store:
        raise HTTPException(status_code=409, detail="product exists")
    store[product.name] = product.price
    return {"name": product.name, "price": product.price}


def _select(store: dict, params: ListParams) -> list[dict]:
    items = [{"name": n, "price": p} for n, p in store.items()]
    if params.q is not None:
        items = [i for i in items if params.q in i["name"]]
    return items


@app.get("/products")
def list_products(store: dict = Depends(get_store), params: ListParams = Depends(list_params)):
    items = sorted(_select(store, params), key=lambda i: i["name"])
    return items[: params.limit]


@app.get("/products/cheap")
def cheap_products(store: dict = Depends(get_store), params: ListParams = Depends(list_params)):
    items = [i for i in _select(store, params) if i["price"] < 10]
    items.sort(key=lambda i: (i["price"], i["name"]))
    return items[: params.limit]
