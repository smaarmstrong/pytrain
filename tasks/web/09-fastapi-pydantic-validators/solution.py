from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

app = FastAPI()


class Customer(BaseModel):
    name: str = Field(min_length=1)
    email: str

    @field_validator("email")
    @classmethod
    def email_has_at(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email must contain @")
        return v


class Item(BaseModel):
    sku: str = Field(min_length=1)
    qty: int = Field(ge=1)
    unit_price: float = Field(gt=0)

    @field_validator("sku")
    @classmethod
    def sku_upper(cls, v: str) -> str:
        return v.upper()


class Order(BaseModel):
    customer: Customer
    items: list[Item] = Field(min_length=1)
    coupon: str | None = None

    @field_validator("coupon")
    @classmethod
    def coupon_known(cls, v: str | None) -> str | None:
        if v is not None and v not in ("SAVE10", "SAVE20"):
            raise ValueError("unknown coupon")
        return v


DISCOUNT = {"SAVE10": 0.10, "SAVE20": 0.20}


@app.post("/orders", status_code=201)
def create_order(order: Order):
    total = sum(i.qty * i.unit_price for i in order.items)
    total *= 1 - DISCOUNT.get(order.coupon, 0.0)
    return {
        "customer": order.customer.name,
        "skus": [i.sku for i in order.items],
        "total": round(total, 2),
    }
