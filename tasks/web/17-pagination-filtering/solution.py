import math

from fastapi import FastAPI, Query

PRODUCTS = [
    {"id": i, "name": f"prod-{i:02d}", "category": ["dairy", "fruit", "veg"][i % 3],
     "price": round(0.5 * i, 2)}
    for i in range(1, 24)
]

app = FastAPI()


@app.get("/products")
def list_products(
    category: str | None = None,
    max_price: float | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=5, ge=1, le=20),
):
    matches = PRODUCTS
    if category is not None:
        matches = [p for p in matches if p["category"] == category]
    if max_price is not None:
        matches = [p for p in matches if p["price"] <= max_price]
    total = len(matches)
    pages = math.ceil(total / page_size)
    start = (page - 1) * page_size
    return {
        "items": matches[start:start + page_size],
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
    }
