from fastapi import FastAPI

PRODUCTS = [
    {"id": i, "name": f"prod-{i:02d}", "category": ["dairy", "fruit", "veg"][i % 3],
     "price": round(0.5 * i, 2)}
    for i in range(1, 24)
]

app = FastAPI()

# GET /products with category/max_price filters and page/page_size — see prompt.md
